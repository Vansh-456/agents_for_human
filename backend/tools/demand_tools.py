from strands import tool
from backend.services.event_service import state_db

@tool
def get_ngo_capacity(ngo_id: str) -> dict:
    """Returns the capacity details for a specific NGO."""
    ngo = state_db.ngos.get(ngo_id)
    if not ngo:
        return {"error": "NGO not found"}
    return {
        "capacity": ngo["capacity"],
        "current_capacity": ngo["current_capacity"]
    }

@tool
def get_all_ngos() -> list:
    """Returns a list of all available NGOs and their capacities."""
    return [{"id": k, **v} for k, v in state_db.ngos.items()]
