from fastapi import APIRouter, HTTPException

from backend.agents.supervisor import rider_unavailable, trigger_pipeline
from backend.services.event_service import state_db

router = APIRouter()


@router.post("/trigger/{scenario}", status_code=202)
def trigger_scenario(scenario: str):
    state_db.reset()
    if scenario == "normal":
        return trigger_pipeline("45 vegetarian meals ready, pickup within 42 minutes", "vendor_1", scenario="normal")
    if scenario == "rider_failure":
        result = trigger_pipeline("45 vegetarian meals ready, pickup within 42 minutes", "vendor_1", scenario="rider_failure")
        if result.get("plan_id"):
            return rider_unavailable(result["plan_id"])
        return result
    if scenario == "safety_block":
        # Represents a verified traffic/road-closure event; it uses the same routing and policy path.
        return trigger_pipeline("30 meals ready, pickup within 25 minutes", "vendor_1", scenario="safety_block", route_delay_mins=30)
    if scenario == "clarification":
        return trigger_pipeline("Prepared meals are available tonight", "vendor_1", scenario="clarification")
    raise HTTPException(404, "Unknown scenario. Use normal, rider_failure, safety_block, or clarification.")
