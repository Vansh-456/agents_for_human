from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.event_service import state_db
from backend.agents.supervisor import trigger_pipeline

router = APIRouter()

class MessagePayload(BaseModel):
    sender_id: str
    text: str

@router.post("/webhook/whatsapp")
def receive_message(payload: MessagePayload):
    # Log to timeline
    state_db.add_timeline_event("WhatsApp", f"Message received from {payload.sender_id}: {payload.text}")
    # Trigger Supervisor / Pipeline
    trigger_pipeline(payload.text, payload.sender_id)
    return {"status": "received"}

@router.get("/state")
def get_global_state():
    return {
        "surplus": state_db.surplus,
        "plans": state_db.plans,
        "ngos": state_db.ngos,
        "vendors": state_db.vendors,
        "riders": state_db.riders
    }

@router.get("/timeline")
def get_timeline():
    return state_db.timeline
