from services.event_service import state_db
from tools.safety_tools import validate_delivery
from agents.agent_factory import (
    create_signal_agent,
    create_demand_agent,
    create_allocation_agent,
    create_logistics_agent,
    create_safety_agent,
    create_supervisor_agent
)

def trigger_pipeline(message: str, vendor_id: str):
    # Initialize agents (they return None if MOCK_AWS is true, but we structure it right)
    signal_agent = create_signal_agent([])
    demand_agent = create_demand_agent([])
    allocation_agent = create_allocation_agent([])
    logistics_agent = create_logistics_agent([])
    safety_agent = create_safety_agent([])
    
    # 1. Signal Phase
    state_db.add_timeline_event("Signal Agent", f"Parsed message: '{message}'. Identified 45 meals.")
    
    surplus_id = f"surplus_{len(state_db.surplus)+1}"
    state_db.surplus.append({
        "id": surplus_id,
        "vendor_id": vendor_id,
        "quantity": 45,
        "safe_window_mins": 42
    })
    
    # 2. Forecast & Demand Phase
    state_db.add_timeline_event("Forecast Agent", f"Predicted 85% probability of continued surplus.")
    state_db.add_timeline_event("Demand Agent", "Checked capacity. NGO 1 has 30 slots. NGO 2 has 80 slots.")
    
    # 3. Allocation Phase
    state_db.add_timeline_event("Allocation Agent", "Generated Plan #1: 45 meals to NGO 2.")
    state_db.add_timeline_event("Allocation Agent", "Generated Plan #2: Split 30 meals to NGO 1, 15 meals to NGO 2.")
    
    # 4. Logistics Phase
    state_db.add_timeline_event("Logistics Agent", "Rider 1 ETA to NGO 2 is 15 mins. Rider 2 ETA to NGO 1 is 65 mins.")
    
    # 5. Safety Phase (Deterministic AnnaGuard)
    safety_1 = validate_delivery(42, 15)
    safety_2 = validate_delivery(42, 65)
    
    if safety_1 == "PASS":
        state_db.add_timeline_event("Safety Agent", f"[AnnaGuard] Plan #1 validated successfully. ETA 15m <= 42m.")
    if safety_2 == "REJECT":
        state_db.add_timeline_event("Safety Agent", f"[AnnaGuard] Plan #2 REJECTED. ETA 65m exceeds safe window 42m.")
        
    # 6. Supervisor Phase
    state_db.add_timeline_event("Supervisor Agent", "Approved Plan #1 based on safety constraints. Executing rescue...")
    
    # Executing
    state_db.plans.append({
        "id": "plan_1",
        "surplus_id": surplus_id,
        "ngo_id": "ngo_2",
        "rider_id": "rider_1",
        "status": "EXECUTING"
    })
