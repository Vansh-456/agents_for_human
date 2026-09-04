import os
from strands import tool
from services.event_service import state_db

@tool
def calculate_eta(rider_id: str, location_lat: float, location_lng: float) -> int:
    """
    Calculates ETA in minutes using a deterministic mock.
    In production, this queries Amazon Location Service.
    """
    MOCK_AWS = os.getenv("MOCK_AWS", "true").lower() == "true"
    
    if not MOCK_AWS:
        # TODO: Implement boto3 Location service calculate_route
        # import boto3
        # client = boto3.client('location')
        pass
        
    # Mock fallback logic for scenarios
    if rider_id == "rider_2":
        return 65 # Simulated slow rider
    return 15 # Simulated fast rider
