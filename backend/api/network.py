from fastapi import APIRouter
from backend.services.event_service import state_db

router = APIRouter()

@router.get("/")
def get_network_state():
    return {
        "vendors": state_db.vendors,
        "ngos": state_db.ngos,
        "riders": state_db.riders,
        "surplus": state_db.surplus,
        "plans": state_db.plans,
        "timeline": state_db.timeline
    }
