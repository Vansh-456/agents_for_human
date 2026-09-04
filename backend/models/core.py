from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Location(BaseModel):
    lat: float
    lng: float

class FoodItem(BaseModel):
    type: str
    quantity: int
    unit: str

class SurplusEvent(BaseModel):
    id: str
    vendor_id: str
    food_items: List[FoodItem]
    available_at: str
    latest_safe_pickup: str
    location: Location
    status: str = "PENDING"

class NGO(BaseModel):
    id: str
    name: str
    location: Location
    capacity: int
    current_capacity: int
    trust_score: float

class Rider(BaseModel):
    id: str
    name: str
    location: Location
    available: bool

class Plan(BaseModel):
    id: str
    surplus_id: str
    ngo_id: str
    rider_id: str
    quantity: int
    eta_mins: int
    rescue_score: float
    safety_status: str
    status: str
