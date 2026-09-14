from strands import tool
from typing import Dict
from backend.services.event_service import state_db
import os

MOCK_AWS = os.getenv("MOCK_AWS", "true").lower() == "true"

@tool
def calculate_community_reliability(participant_id: str) -> Dict:
    """
    Evaluates the historical reliability of a community participant (like an NGO)
    based on successful pickups, cancellations, and on-time arrivals.
    Returns a trust score between 0 and 1.
    """
    # For hackathon demo, mock specific community scores
    if participant_id == "ngo_1":
        return {
            "participant_id": participant_id,
            "trust_score": 0.72,
            "factors": {
                "punctuality": 0.65,
                "response": 0.80,
                "completion": 0.70
            },
            "insight": "Historical data shows frequent delays. Lower priority for urgent safety windows."
        }
    
    if participant_id == "ngo_2":
        return {
            "participant_id": participant_id,
            "trust_score": 0.95,
            "factors": {
                "punctuality": 0.98,
                "response": 0.90,
                "completion": 0.96
            },
            "insight": "Highly reliable community partner. Preferred for time-sensitive allocations."
        }
        
    return {
        "participant_id": participant_id,
        "trust_score": 0.85,
        "factors": {
            "punctuality": 0.85,
            "response": 0.85,
            "completion": 0.85
        },
        "insight": "Average reliability."
    }
