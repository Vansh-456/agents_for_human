from datetime import datetime, timezone
from uuid import uuid4

from backend.repositories.base import Repository


class InMemoryRepository(Repository):

    def __init__(self):
        self.vendors = {}
        self.ngos = {}
        self.riders = {}
        self.surplus = {}
        self.allocations = {}
        self.events = []

    # ---------- Participants ----------

    def get_vendor(self, vendor_id: str):
        return self.vendors.get(vendor_id)

    def get_ngo(self, ngo_id: str):
        return self.ngos.get(ngo_id)

    def get_rider(self, rider_id: str):
        return self.riders.get(rider_id)

    def save_vendor(self, vendor_id: str, data: dict):
        self.vendors[vendor_id] = data

    def save_ngo(self, ngo_id: str, data: dict):
        self.ngos[ngo_id] = data

    def save_rider(self, rider_id: str, data: dict):
        self.riders[rider_id] = data

    # ---------- Surplus ----------

    def save_surplus(self, surplus_id: str, data: dict):
        self.surplus[surplus_id] = data

    def get_surplus(self, surplus_id: str):
        return self.surplus.get(surplus_id)

    def get_all_surplus(self):
        return list(self.surplus.values())

    # ---------- Allocations ----------

    def save_allocation(self, allocation_id: str, data: dict):
        self.allocations[allocation_id] = data

    def get_allocation(self, allocation_id: str):
        return self.allocations.get(allocation_id)

    def get_all_allocations(self):
        return list(self.allocations.values())

    # ---------- Events ----------

    def record_event(
        self,
        event_type: str,
        actor: str,
        payload: dict
    ):
        event = {
            "event_id": f"evt_{uuid4().hex[:8]}",
            "event_type": event_type,
            "actor": actor,
            "payload": payload,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.events.append(event)
        return event

    def get_events(self):
        return list(self.events)

    # ---------- Reset ----------

    def reset(self):
        self.surplus.clear()
        self.allocations.clear()
        self.events.clear()