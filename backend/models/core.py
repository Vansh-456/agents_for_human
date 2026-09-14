from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime, timezone

class BaseRecord(BaseModel):
    workflow_id: str
    correlation_id: str
    actor: str
    version: int = 1
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_type: str = "operational"
    source_reference: Optional[str] = None
    idempotency_key: Optional[str] = None

class Location(BaseModel):
    lat: float
    lng: float
    address: Optional[str] = None

class Evidence(BaseModel):
    temperature: Optional[float] = None
    photo_url: Optional[str] = None
    packing_checklist_verified: bool = False

class FoodBatch(BaseModel):
    id: str
    type: str
    category: Literal["vegetarian", "non-vegetarian", "prepared_meal"]
    quantity: int
    unit: str
    allergens: List[str] = []
    temperature_req: Optional[str] = None
    packaging: str = "standard"

class SurplusEvent(BaseRecord):
    id: str
    vendor_id: str
    batches: List[FoodBatch]
    available_at: str
    latest_safe_pickup: str
    location: Location
    evidence: Evidence = Field(default_factory=Evidence)
    status: Literal["REPORTED", "NEEDS_CLARIFICATION", "VERIFIED", "CANDIDATES_READY"] = "REPORTED"

class RecipientCapacity(BaseRecord):
    id: str
    ngo_id: str
    capacity: int
    current_capacity: int
    accepted_food_categories: List[str]
    operating_hours: str

class Organisation(BaseRecord):
    id: str
    type: Literal["donor", "recipient", "logistics"]
    name: str
    location: Location
    trust_score: float = 1.0

class Rider(BaseRecord):
    id: str
    name: str
    location: Location
    available: bool
    capacity: int
    vehicle_type: str

class RiderReservation(BaseRecord):
    id: str
    rider_id: str
    workflow_id: str
    expires_at: str
    status: Literal["ACTIVE", "RELEASED", "CONSUMED"]

class AllocationLeg(BaseModel):
    origin: Location
    destination: Location
    eta_mins: int
    status: str

class Decision(BaseModel):
    status: Literal["PASS", "REVIEW", "BLOCK"]
    reasons: List[str] = []
    safety_margin_mins: Optional[int] = None

class AllocationPlan(BaseRecord):
    id: str
    surplus_id: str
    ngo_id: str
    rider_id: str
    quantity: int
    eta_mins: int
    rescue_score: float
    legs: List[AllocationLeg] = []
    safety: Decision
    safety_status: str
    status: Literal["PROPOSED", "SAFETY_PASS", "SAFETY_REVIEW", "SAFETY_BLOCKED", "RESERVED", "ASSIGNED", "ACCEPTED", "PICKED_UP", "IN_TRANSIT", "DELIVERED", "FAILED", "CANCELLED", "EXPIRED"] = "PROPOSED"

class DomainEvent(BaseModel):
    id: str
    type: str
    timestamp: str
    payload: Dict[str, Any]
    source: str
