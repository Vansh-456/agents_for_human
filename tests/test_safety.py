import pytest
from backend.tools.safety_tools import evaluate_delivery

def test_safety_deterministic_pass():
    """Verify that a safe route returns a deterministic PASS status."""
    decision = evaluate_delivery(
        quantity=50,
        available_capacity=100,
        eta_mins=15,
        remaining_safe_window_mins=60,
        rider_available=True,
        food_category="prepared_meal",
        evidence_verified=True
    )
    assert decision.status == "PASS"
    assert decision.safety_margin_mins == 45
    assert not decision.reasons

def test_safety_deterministic_review():
    """Verify that a tight margin returns a REVIEW status."""
    decision = evaluate_delivery(
        quantity=50,
        available_capacity=100,
        eta_mins=55,
        remaining_safe_window_mins=60,
        rider_available=True,
        food_category="prepared_meal",
        evidence_verified=True
    )
    assert decision.status == "REVIEW"
    assert decision.safety_margin_mins == 5
    assert "safe margin is below 10 minutes" in decision.reasons

def test_safety_deterministic_block_expired():
    """Verify that a route exceeding the safe window is unconditionally BLOCKED."""
    decision = evaluate_delivery(
        quantity=50,
        available_capacity=100,
        eta_mins=90,
        remaining_safe_window_mins=60,
        rider_available=True,
        food_category="prepared_meal",
        evidence_verified=True
    )
    assert decision.status == "BLOCK"
    assert "route ETA exceeds remaining safe window" in decision.reasons

def test_safety_deterministic_block_capacity():
    """Verify that a route exceeding recipient capacity is BLOCKED."""
    decision = evaluate_delivery(
        quantity=200,
        available_capacity=100,
        eta_mins=15,
        remaining_safe_window_mins=60,
        rider_available=True,
        food_category="prepared_meal",
        evidence_verified=True
    )
    assert decision.status == "BLOCK"
    assert "recipient capacity is insufficient" in decision.reasons

def test_safety_deterministic_block_missing_rider():
    """Verify that lack of a rider blocks the plan."""
    decision = evaluate_delivery(
        quantity=50,
        available_capacity=100,
        eta_mins=15,
        remaining_safe_window_mins=60,
        rider_available=False,
        food_category="prepared_meal",
        evidence_verified=True
    )
    assert decision.status == "BLOCK"
    assert "rider is unavailable" in decision.reasons
