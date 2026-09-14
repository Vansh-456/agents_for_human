from strands import tool
from datetime import datetime

@tool
def predict_surplus_likelihood(vendor_id: str) -> dict:
    """
    Predicts the likelihood of food surplus for a given vendor based on historical community data and time of day.
    Returns a probability and expected quantity.
    """
    # For hackathon demo, mock a proactive forecast
    current_hour = datetime.now().hour
    
    if current_hour >= 18 and current_hour <= 22:
        return {
            "vendor_id": vendor_id,
            "prediction": {
                "probability": 0.85,
                "expected_quantity_meals": 45,
                "time_window": "20:30-21:30"
            },
            "insight": "High probability of surplus due to evening dinner service closing."
        }
        
    return {
        "vendor_id": vendor_id,
        "prediction": {
            "probability": 0.20,
            "expected_quantity_meals": 10,
            "time_window": f"{current_hour+1}:00-{current_hour+2}:00"
        },
        "insight": "Low probability during off-peak hours."
    }
