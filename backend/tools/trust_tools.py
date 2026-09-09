from strands import tool
from backend.services.event_service import state_db

@tool
def get_trust_score(participant_id: str) -> float:
    """Returns the trust/reliability score for a vendor or NGO."""
    if participant_id in state_db.vendors:
        return state_db.vendors[participant_id].get("trust_score", 0.5)
    if participant_id in state_db.ngos:
        return state_db.ngos[participant_id].get("trust_score", 0.5)
    return 0.5
