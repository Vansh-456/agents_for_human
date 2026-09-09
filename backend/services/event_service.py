from datetime import datetime

from backend.repositories.dynamodb_repository import DynamoDBRepository


class StateDB:
    """
    Compatibility layer for the existing application.

    The existing API/agent code can continue using StateDB while
    persistence is handled by the repository layer.
    """

    def __init__(self, repository=None):
        self.repository = repository or DynamoDBRepository()

        self.vendors = {
            "vendor_1": {
                "name": "Restaurant A",
                "location": {"lat": 28.61, "lng": 77.23},
                "trust_score": 0.95
            },
            "vendor_2": {
                "name": "Canteen B",
                "location": {"lat": 28.62, "lng": 77.21},
                "trust_score": 0.88
            }
        }

        self.ngos = {
            "ngo_1": {
                "name": "Shelter X",
                "location": {"lat": 28.63, "lng": 77.22},
                "capacity": 50,
                "current_capacity": 20,
                "trust_score": 0.94
            },
            "ngo_2": {
                "name": "Food Bank Y",
                "location": {"lat": 28.60, "lng": 77.25},
                "capacity": 100,
                "current_capacity": 80,
                "trust_score": 0.90
            }
        }

        self.riders = {
            "rider_1": {
                "name": "Rider John",
                "location": {"lat": 28.615, "lng": 77.225},
                "available": True
            },
            "rider_2": {
                "name": "Rider Sarah",
                "location": {"lat": 28.605, "lng": 77.245},
                "available": True
            }
        }

        self.surplus = []
        self.plans = []
        self.timeline = []

        self._persist_initial_state()

    def _persist_initial_state(self):
        """Persist demo participants into the repository."""

        for vendor_id, vendor in self.vendors.items():
            self.repository.save_vendor(vendor_id, vendor)

        for ngo_id, ngo in self.ngos.items():
            self.repository.save_ngo(ngo_id, ngo)

        for rider_id, rider in self.riders.items():
            self.repository.save_rider(rider_id, rider)

    def add_timeline_event(self, agent: str, message: str):
        """
        Preserve the existing timeline API while also recording
        the event in persistent storage.
        """

        timestamp = datetime.now().strftime("%H:%M:%S")

        timeline_event = {
            "timestamp": timestamp,
            "agent": agent,
            "message": message
        }

        self.timeline.append(timeline_event)

        self.repository.record_event(
            event_type="TIMELINE_EVENT",
            actor=agent,
            payload={
                "message": message,
                "timestamp": timestamp
            }
        )

        print(f"[{timestamp}] {agent}: {message}")

    def add_surplus(self, surplus_id: str, surplus_data: dict):
        """Add surplus to both application state and persistence."""

        self.surplus.append(surplus_data)

        self.repository.save_surplus(
            surplus_id,
            surplus_data
        )

        self.repository.record_event(
            event_type="SURPLUS_CREATED",
            actor=surplus_data.get("vendor_id", "system"),
            payload=surplus_data
        )

    def add_plan(self, plan_id: str, plan_data: dict):
        """Add allocation plan to both application state and persistence."""

        self.plans.append(plan_data)

        self.repository.save_allocation(
            plan_id,
            plan_data
        )

        self.repository.record_event(
            event_type="ALLOCATION_CREATED",
            actor="system",
            payload=plan_data
        )

    def reset(self):
        self.surplus = []
        self.plans = []
        self.timeline = []

        for r in self.riders.values():
            r["available"] = True

        self.ngos["ngo_1"]["current_capacity"] = 20
        self.ngos["ngo_2"]["current_capacity"] = 80

        self.repository.reset()

        self._persist_initial_state()


state_db = StateDB()