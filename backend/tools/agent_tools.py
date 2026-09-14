from strands import tool
from typing import List, Dict, Any
from backend.services.event_service import state_db
import uuid

@tool
def create_surplus_event(vendor_id: str, quantity: int, safe_window_mins: int) -> str:
    """
    Creates a new food surplus event.
    Returns the generated surplus_id.
    """
    surplus_id = f"surplus_{len(state_db.surplus) + 1}_{uuid.uuid4().hex[:4]}"
    surplus_data = {
        "id": surplus_id,
        "vendor_id": vendor_id,
        "quantity": quantity,
        "safe_window_mins": safe_window_mins
    }
    state_db.add_surplus(surplus_id, surplus_data)
    return surplus_id

@tool
def query_ngo_capacity() -> List[Dict[str, Any]]:
    """
    Returns a list of all NGOs and their current available capacity.
    """
    results = []
    for ngo_id, ngo_data in state_db.ngos.items():
        results.append({
            "ngo_id": ngo_id,
            "name": ngo_data.get("name"),
            "current_capacity": ngo_data.get("current_capacity", 0),
            "location": ngo_data.get("location")
        })
    return results

@tool
def find_available_riders() -> List[Dict[str, Any]]:
    """
    Returns a list of all currently available riders.
    """
    results = []
    for rider_id, rider_data in state_db.riders.items():
        if rider_data.get("available", False):
            results.append({
                "rider_id": rider_id,
                "name": rider_data.get("name"),
                "location": rider_data.get("location")
            })
    return results

@tool
def calculate_eta_mins(origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float) -> int:
    """
    Calculates estimated travel time in minutes between two coordinates.
    Currently uses a simple mock heuristic (distance * factor).
    """
    # Simple Manhattan distance heuristic for mock ETA
    dist = abs(origin_lat - dest_lat) + abs(origin_lng - dest_lng)
    # Approx 1 degree = 111km, assume 30km/h speed -> 1 degree = 222 mins
    return int(max(10, dist * 222))

@tool
def propose_allocation_plan(surplus_id: str, ngo_id: str, rider_id: str) -> str:
    """
    Proposes a new allocation plan. This does not execute it, but creates a record of the proposal.
    Returns the plan_id.
    """
    plan_id = f"plan_{len(state_db.plans) + 1}_{uuid.uuid4().hex[:4]}"
    plan_data = {
        "id": plan_id,
        "surplus_id": surplus_id,
        "ngo_id": ngo_id,
        "rider_id": rider_id,
        "status": "PROPOSED"
    }
    # We don't use add_plan here because it emits an ALLOCATION_CREATED event and commits it fully, 
    # but the proposal needs safety validation first. For simplicity in the demo, we will just return the dict string.
    return str(plan_data)
