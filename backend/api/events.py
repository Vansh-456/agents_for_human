from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.agents.supervisor import rider_unavailable, trigger_pipeline
from backend.services.event_service import state_db

router = APIRouter()


class MessagePayload(BaseModel):
    sender_id: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=3, max_length=2000)
    idempotency_key: str | None = Field(default=None, max_length=128)


class PlanStatusPayload(BaseModel):
    status: Literal["ACCEPTED", "PICKED_UP", "IN_TRANSIT", "DELIVERED", "CANCELLED", "FAILED"]


@router.post("/webhook/whatsapp", status_code=202)
def receive_message(payload: MessagePayload):
    # Signature validation belongs at the API gateway/webhook adapter boundary.
    state_db.add_timeline_event("WhatsApp", "Donation message received.", sender_id=payload.sender_id)
    return trigger_pipeline(payload.text, payload.sender_id)


@router.get("/state")
def get_global_state():
    return {"surplus": state_db.surplus, "plans": state_db.plans, "ngos": state_db.ngos,
            "vendors": state_db.vendors, "riders": state_db.riders}


@router.get("/timeline")
def get_timeline():
    return state_db.timeline


@router.get("/plans/{plan_id}")
def get_plan(plan_id: str):
    plan = state_db.repository.get_allocation(plan_id)
    if not plan:
        raise HTTPException(404, "Plan not found")
    return plan


@router.post("/plans/{plan_id}/status")
def update_plan_status(plan_id: str, payload: PlanStatusPayload):
    plan = state_db.repository.get_allocation(plan_id)
    if not plan:
        raise HTTPException(404, "Plan not found")
    allowed = {"ASSIGNED": {"ACCEPTED", "CANCELLED", "FAILED"}, "ACCEPTED": {"PICKED_UP", "CANCELLED", "FAILED"},
               "PICKED_UP": {"IN_TRANSIT", "FAILED"}, "IN_TRANSIT": {"DELIVERED", "FAILED"}}
    if payload.status not in allowed.get(plan["status"], set()):
        raise HTTPException(409, f"Cannot transition {plan['status']} to {payload.status}")
    plan["status"] = payload.status
    state_db.add_plan(plan_id, plan)
    state_db.add_timeline_event("Operations", f"Plan status updated to {payload.status}.", workflow_id=plan["workflow_id"], plan_id=plan_id)
    return plan


@router.post("/plans/{plan_id}/rider-unavailable", status_code=202)
def replan(plan_id: str):
    try:
        return rider_unavailable(plan_id)
    except ValueError as error:
        raise HTTPException(404, str(error)) from error
