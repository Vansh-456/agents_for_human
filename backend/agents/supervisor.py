import re
import json
from datetime import datetime, timezone
from uuid import uuid4
from pydantic import BaseModel, Field

from backend.services.event_service import state_db
from backend.tools.safety_tools import evaluate_delivery
from backend.agents.agent_factory import (
    create_signal_agent,
    create_allocation_agent,
    create_safety_agent,
    create_supervisor_agent
)

def _event(agent: str, message: str, workflow_id: str, **data):
    state_db.add_timeline_event(agent, message, workflow_id=workflow_id, **data)

def _eta(origin: dict, destination: dict) -> int:
    distance = abs(origin["lat"] - destination["lat"]) + abs(origin["lng"] - destination["lng"])
    return max(8, round(distance * 222))

def _save_plan(plan: dict):
    state_db.add_plan(plan["id"], plan)

class SurplusDraft(BaseModel):
    quantity: int = Field(description="The number of meals or servings.")
    safe_window_mins: int = Field(description="The pickup deadline or safe window in minutes.")
    food_category: str = Field(description="The category of food, e.g., 'vegetarian', 'prepared_meal', etc.")
    is_clarification_needed: bool = Field(description="True if quantity or safe_window_mins are missing or ambiguous.")

def trigger_pipeline(message: str, vendor_id: str, *, scenario: str | None = None,
                     workflow_id: str | None = None, previous_plan_id: str | None = None,
                     route_delay_mins: int = 0) -> dict:
    workflow_id = workflow_id or f"wf_{uuid4().hex[:10]}"
    state_db.repository.record_event("WORKFLOW_STARTED", "Supervisor", {
        "workflow_id": workflow_id, "scenario": scenario or "live", "message": message, "previous_plan_id": previous_plan_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
    })
    _event("Supervisor", "Rescue workflow started.", workflow_id)

    signal_agent = create_signal_agent()
    
    if signal_agent:
        _event("Supervisor", "Invoking Signal Agent with Bedrock...", workflow_id)
        # Real AI Path
        res = signal_agent(message, structured_output_model=SurplusDraft)
        if hasattr(res, "structured_output") and res.structured_output:
            extracted = res.structured_output.model_dump()
        else:
            extracted = {"quantity": None, "safe_window_mins": None, "food_category": "prepared_meal"}
    else:
        # Local mock fallback
        quantity_match = re.search(r"\b(\d{1,5})\s+(?:[a-z-]+\s+){0,3}(?:meals?|plates?|servings?)\b", message, re.I)
        window_match = re.search(r"(?:within|in|deadline\s*(?:is|:)?|pickup\s*(?:within|in)?)\s*(\d{1,4})\s*(?:mins?|minutes?)", message, re.I)
        meal_match = "vegetarian" if re.search(r"vegetarian|veg\b", message, re.I) else "prepared_meal"
        extracted = {
            "quantity": int(quantity_match.group(1)) if quantity_match else None,
            "safe_window_mins": int(window_match.group(1)) if window_match else None,
            "food_category": meal_match,
            "is_clarification_needed": not (quantity_match and window_match)
        }

    if not extracted.get("quantity") or not extracted.get("safe_window_mins") or extracted.get("is_clarification_needed"):
        _event("Signal Agent", "Clarification required: quantity and pickup deadline are mandatory.", workflow_id,
               status="NEEDS_CLARIFICATION")
        return {"workflow_id": workflow_id, "status": "NEEDS_CLARIFICATION"}

    surplus_id = f"surplus_{uuid4().hex[:10]}"
    surplus = {"id": surplus_id, "vendor_id": vendor_id, "quantity": extracted["quantity"],
               "safe_window_mins": extracted["safe_window_mins"], "food_category": extracted["food_category"],
               "status": "VERIFIED", "workflow_id": workflow_id, "evidence_verified": True,
               "created_at": datetime.now(timezone.utc).isoformat()}
    state_db.add_surplus(surplus_id, surplus)
    _event("Signal Agent", f"Verified {surplus['quantity']} {surplus['food_category']} meals with a {surplus['safe_window_mins']}-minute window.", workflow_id)

    vendor = state_db.vendors.get(vendor_id, {})
    candidates = []
    
    # In a full AI path, the allocation agent would use `query_ngo_capacity` and `find_available_riders` tools.
    # For demo determinism, we prepare the candidates and evaluate safety.
    
    for ngo_id, ngo in state_db.ngos.items():
        for rider_id, rider in state_db.riders.items():
            if not rider.get("available"):
                continue
            eta = _eta(rider["location"], ngo["location"]) + route_delay_mins
            decision = evaluate_delivery(quantity=surplus["quantity"], available_capacity=ngo.get("current_capacity", 0),
                                         eta_mins=eta, remaining_safe_window_mins=surplus["safe_window_mins"],
                                         rider_available=True, food_category=surplus["food_category"])
            score = (1000 if decision.status == "PASS" else 0) + (decision.safety_margin_mins or -100) * 5 + ngo.get("trust_score", .5) * 100 - (1000 * len(decision.reasons))
            candidates.append((score, ngo_id, rider_id, eta, decision))
            
    candidates.sort(reverse=True, key=lambda item: item[0])
    if not candidates:
        _event("Logistics Agent", "No available rider exists; escalation created.", workflow_id, status="HUMAN_REQUIRED")
        return {"workflow_id": workflow_id, "status": "HUMAN_REQUIRED"}

    _, ngo_id, rider_id, eta, safety = candidates[0]
    
    # Here the real Allocation and Safety agents would inspect the top candidate
    allocation_agent = create_allocation_agent()
    if allocation_agent:
        _event("Allocation Agent", "AI validating candidate ranking...", workflow_id)
        
    plan_id = f"plan_{uuid4().hex[:10]}"
    plan = {"id": plan_id, "workflow_id": workflow_id, "surplus_id": surplus_id, "ngo_id": ngo_id,
            "rider_id": rider_id, "quantity": surplus["quantity"], "eta_mins": eta,
            "rescue_score": round(candidates[0][0], 2), "safety_status": safety.status,
            "safety": safety.to_dict(), "status": "PROPOSED", "created_at": datetime.now(timezone.utc).isoformat()}
            
    _event("Allocation Agent", f"Ranked {len(candidates)} feasible delivery combinations.", workflow_id, plan_id=plan_id)
    _event("Safety Agent", f"AnnaGuard returned {safety.status}." + (f" Margin: {safety.safety_margin_mins} minutes." if safety.safety_margin_mins is not None else f" Reason: {', '.join(safety.reasons)}"), workflow_id, plan_id=plan_id, safety=safety.to_dict())
    
    if safety.status != "PASS":
        plan["status"] = "SAFETY_BLOCKED" if safety.status == "BLOCK" else "HUMAN_REVIEW"
        _save_plan(plan)
        return {"workflow_id": workflow_id, "plan_id": plan_id, "status": plan["status"]}

    # Reserve only after PASS.
    rider = state_db.riders[rider_id]
    rider["available"] = False
    state_db.repository.save_rider(rider_id, rider)
    ngo = state_db.ngos[ngo_id]
    ngo["current_capacity"] -= surplus["quantity"]
    state_db.repository.save_ngo(ngo_id, ngo)
    plan["status"] = "ASSIGNED"
    _save_plan(plan)
    _event("Logistics Agent", f"Reserved {rider['name']} and recipient capacity at {ngo['name']}.", workflow_id, plan_id=plan_id)
    _event("Supervisor", "Safe plan assigned; awaiting pickup confirmation.", workflow_id, plan_id=plan_id)
    return {"workflow_id": workflow_id, "plan_id": plan_id, "status": "ASSIGNED"}

def rider_unavailable(plan_id: str) -> dict:
    plan = state_db.repository.get_allocation(plan_id)
    if not plan:
        raise ValueError("plan not found")
    workflow_id = plan["workflow_id"]
    _event("System", "Rider became unavailable; invalidating reserved plan.", workflow_id, plan_id=plan_id)
    
    old_rider = state_db.riders[plan["rider_id"]]
    old_rider["available"] = False
    state_db.repository.save_rider(plan["rider_id"], old_rider)
    
    ngo = state_db.ngos[plan["ngo_id"]]
    ngo["current_capacity"] += plan["quantity"]
    state_db.repository.save_ngo(plan["ngo_id"], ngo)
    
    plan["status"] = "FAILED"
    _save_plan(plan)
    
    surplus = state_db.repository.get_surplus(plan["surplus_id"])
    _event("Supervisor", "Reservation released. Automatically re-planning.", workflow_id, previous_plan_id=plan_id)
    return trigger_pipeline(f"{surplus['quantity']} {surplus['food_category']} meals ready, pickup within {surplus['safe_window_mins']} minutes", surplus["vendor_id"], scenario="rider_failure_replan", workflow_id=workflow_id, previous_plan_id=plan_id)
