"""Deterministic safety control plane.

This module deliberately contains no model calls.  A model may suggest a plan,
but only this policy can make it executable.
"""
from dataclasses import asdict, dataclass
from typing import Any

from strands import tool


@dataclass(frozen=True)
class SafetyDecision:
    status: str
    reasons: list[str]
    safety_margin_mins: int | None
    policy_version: str = "annaguard-1.0"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_delivery(*, quantity: int, available_capacity: int, eta_mins: int,
                      remaining_safe_window_mins: int, rider_available: bool,
                      food_category: str = "prepared_meal",
                      evidence_verified: bool = True) -> SafetyDecision:
    """Return a machine-readable, deterministic safety outcome."""
    reasons: list[str] = []
    if quantity <= 0:
        reasons.append("quantity must be positive")
    if not evidence_verified:
        reasons.append("required freshness evidence is not verified")
    if food_category.strip() == "":
        reasons.append("food category is missing")
    if not rider_available:
        reasons.append("rider is unavailable")
    if available_capacity < quantity:
        reasons.append("recipient capacity is insufficient")
    if remaining_safe_window_mins <= 0:
        reasons.append("food is outside its usable window")
    if eta_mins > remaining_safe_window_mins:
        reasons.append("route ETA exceeds remaining safe window")
    if reasons:
        return SafetyDecision("BLOCK", reasons, None)

    margin = remaining_safe_window_mins - eta_mins
    if margin < 10:
        return SafetyDecision("REVIEW", ["safe margin is below 10 minutes"], margin)
    return SafetyDecision("PASS", [], margin)


@tool
def validate_delivery(food_safe_window_mins: int, eta_mins: int) -> str:
    """Compatibility tool returning PASS only for a safe deterministic result."""
    return evaluate_delivery(
        quantity=1, available_capacity=1, eta_mins=eta_mins,
        remaining_safe_window_mins=food_safe_window_mins, rider_available=True,
    ).status
