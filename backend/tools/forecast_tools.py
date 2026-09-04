from strands import tool

@tool
def predict_surplus(vendor_id: str, time_of_day: str) -> dict:
    """Predicts likelihood of surplus based on historical data."""
    # Mocking prediction for hackathon
    probability = 0.85 if vendor_id == "vendor_1" else 0.40
    return {
        "probability": probability,
        "expected_quantity": 40 if probability > 0.5 else 10,
        "time_window": "20:00-21:00"
    }
