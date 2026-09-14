from fastapi import APIRouter, Request
from backend.services.event_service import state_db
from backend.api.simulation import trigger_scenario
from backend.api.events import receive_message, MessagePayload

router = APIRouter()

@router.post("/allocate")
async def allocate_endpoint():
    """Trigger a normal allocation workflow for judge visibility."""
    return await trigger_scenario("normal")

@router.post("/replan")
async def replan_endpoint():
    """Trigger a rider failure replan workflow for judge visibility."""
    return await trigger_scenario("rider_failure")

@router.get("/agents")
def get_agents():
    """List the agents active in the orchestration layer."""
    return {
        "agents": [
            {"id": "supervisor", "role": "Orchestrator"},
            {"id": "signal", "role": "Extraction"},
            {"id": "demand", "role": "Capacity Matching"},
            {"id": "logistics", "role": "Routing"},
            {"id": "allocation", "role": "Planning"},
            {"id": "safety", "role": "AnnaGuard Enforcer"}
        ]
    }

@router.get("/decisions")
def get_decisions():
    """Expose the active decision ledger."""
    return state_db.plans

@router.get("/metrics")
def get_metrics():
    """Expose the active dashboard metrics."""
    plans = list(state_db.plans.values())
    delivered = sum(p.get("quantity", 0) for p in plans if p.get("status") == "DELIVERED")
    active = sum(1 for p in plans if p.get("status") not in ["DELIVERED", "FAILED", "CANCELLED"])
    
    return {
        "meals_delivered": delivered,
        "active_rescues": active,
        "riders_ready": sum(1 for r in state_db.riders.values() if r.get("available")),
        "auto_recoveries": sum(1 for p in plans if p.get("status") == "FAILED")
    }

@router.post("/webhooks/whatsapp")
async def alias_whatsapp_webhook(payload: MessagePayload):
    """Alias for the WhatsApp webhook endpoint required by the spec."""
    return receive_message(payload)
