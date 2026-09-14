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
        self._persist_initial_state()

    @property
    def vendors(self):
        return self.repository.get_all_vendors()

    @property
    def ngos(self):
        return self.repository.get_all_ngos()

    @property
    def riders(self):
        return self.repository.get_all_riders()

    @property
    def surplus(self):
        return self.repository.get_all_surplus()

    @property
    def plans(self):
        return self.repository.get_all_allocations()

    @property
    def timeline(self):
        return [
            {
                "timestamp": event["payload"].get("timestamp"),
                "agent": event["actor"],
                "message": event["payload"].get("message")
            }
            for event in self.repository.get_events()
            if event["event_type"] == "TIMELINE_EVENT"
        ]

    def _persist_initial_state(self):
        """Persist demo participants into the repository if they don't exist."""
        vendors = self.repository.get_all_vendors()
        if not vendors:
            self.repository.save_vendor("vendor_1", {"name": "Restaurant A", "location": {"lat": 28.61, "lng": 77.23}, "trust_score": 0.95})
            self.repository.save_vendor("vendor_2", {"name": "Canteen B", "location": {"lat": 28.62, "lng": 77.21}, "trust_score": 0.88})
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
        self._persist_initial_state()

    @property
    def vendors(self):
        return self.repository.get_all_vendors()

    @property
    def ngos(self):
        return self.repository.get_all_ngos()

    @property
    def riders(self):
        return self.repository.get_all_riders()

    @property
    def surplus(self):
        return self.repository.get_all_surplus()

    @property
    def plans(self):
        return self.repository.get_all_allocations()

    @property
    def timeline(self):
        return [
            {
                "timestamp": event["payload"].get("timestamp"),
                "agent": event["actor"],
                "message": event["payload"].get("message")
            }
            for event in self.repository.get_events()
            if event["event_type"] == "TIMELINE_EVENT"
        ]

    def _persist_initial_state(self):
        """Persist demo participants into the repository if they don't exist."""
        vendors = self.repository.get_all_vendors()
        if not vendors:
            self.repository.save_vendor("vendor_1", {"name": "Restaurant A", "location": {"lat": 28.61, "lng": 77.23}, "trust_score": 0.95})
            self.repository.save_vendor("vendor_2", {"name": "Canteen B", "location": {"lat": 28.62, "lng": 77.21}, "trust_score": 0.88})

        ngos = self.repository.get_all_ngos()
        if not ngos:
            self.repository.save_ngo("ngo_1", {"name": "Shelter X", "location": {"lat": 28.63, "lng": 77.22}, "capacity": 50, "current_capacity": 20, "trust_score": 0.94})
            self.repository.save_ngo("ngo_2", {"name": "Food Bank Y", "location": {"lat": 28.60, "lng": 77.25}, "capacity": 100, "current_capacity": 80, "trust_score": 0.90})

        riders = self.repository.get_all_riders()
        if not riders:
            self.repository.save_rider("rider_1", {"name": "Rider John", "location": {"lat": 28.615, "lng": 77.225}, "available": True})
            self.repository.save_rider("rider_2", {"name": "Rider Sarah", "location": {"lat": 28.605, "lng": 77.245}, "available": True})

        plans = self.repository.get_all_allocations()
        if not plans:
            self.repository.save_allocation("plan_hist_1", {
                "id": "plan_hist_1",
                "workflow_id": "wf_hist_1",
                "surplus_id": "surplus_hist_1",
                "ngo_id": "ngo_1",
                "rider_id": "rider_1",
                "quantity": 250,
                "eta_mins": 15,
                "safety_status": "PASS",
                "status": "DELIVERED"
            })
            self.repository.save_allocation("plan_hist_2", {
                "id": "plan_hist_2",
                "workflow_id": "wf_hist_2",
                "surplus_id": "surplus_hist_2",
                "ngo_id": "ngo_2",
                "rider_id": "rider_2",
                "quantity": 77,
                "eta_mins": 12,
                "safety_status": "PASS",
                "status": "DELIVERED"
            })
            self.repository.record_event(
                event_type="TIMELINE_EVENT",
                actor="System",
                payload={"message": "System booted. Restored 327 historically delivered meals.", "timestamp": datetime.now().strftime("%H:%M:%S")}
            )

    def add_timeline_event(self, agent: str, message: str, **context):
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.repository.record_event(
            event_type="TIMELINE_EVENT",
            actor=agent,
            payload={
                "message": message,
                "timestamp": timestamp,
                **context,
            }
        )
        print(f"[{timestamp}] {agent}: {message}")

    def add_surplus(self, surplus_id: str, surplus_data: dict):
        """Add surplus to both application state and persistence."""
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
        self.repository.reset()
        self._persist_initial_state()


state_db = StateDB()
