from strands import tool

@tool
def validate_delivery(food_safe_window_mins: int, eta_mins: int) -> str:
    """
    Deterministic safety validation.
    Returns "REJECT" if the ETA exceeds the safe handling window, else "PASS".
    """
    if food_safe_window_mins <= 0:
        return "REJECT"
    if eta_mins > food_safe_window_mins:
        return "REJECT"
    return "PASS"
