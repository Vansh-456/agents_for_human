from fastapi import APIRouter
from services.event_service import state_db
from agents.supervisor import trigger_pipeline
from tools.safety_tools import validate_delivery

router = APIRouter()

@router.post("/trigger/normal")
def trigger_normal():
    state_db.reset()
    trigger_pipeline("45 meals ready at Restaurant A", "vendor_1")
    return {"status": "started"}

@router.post("/trigger/rider_failure")
def trigger_rider_failure():
    state_db.reset()
    state_db.add_timeline_event("Signal Agent", "Parsed 45 meals.")
    state_db.add_timeline_event("Allocation Agent", "Assigned Rider 1 to NGO 1.")
    state_db.add_timeline_event("System", "RIDER_UNAVAILABLE event for Rider 1.")
    state_db.add_timeline_event("Supervisor", "Detected plan invalidation. Triggering Re-plan.")
    state_db.add_timeline_event("Logistics Agent", "Found alternative: Rider 2. ETA 18 min.")
    safety = validate_delivery(42, 18)
    state_db.add_timeline_event("Safety Agent", f"Alternative plan {safety}. ETA 18m <= 42m window.")
    state_db.add_timeline_event("Supervisor", "Executing alternative plan.")
    return {"status": "replan_executed"}

@router.post("/trigger/safety_block")
def trigger_safety_block():
    state_db.reset()
    state_db.add_timeline_event("Signal Agent", "Parsed 30 meals.")
    state_db.add_timeline_event("Logistics Agent", "Closest rider ETA is 38 minutes.")
    state_db.add_timeline_event("Safety Agent", "SAFETY BLOCK: Reason: ETA (38m) exceeds remaining safe window (25m). Action: Reject.")
    state_db.add_timeline_event("Supervisor", "Escalating or Searching Alternative.")
    return {"status": "safety_blocked"}
