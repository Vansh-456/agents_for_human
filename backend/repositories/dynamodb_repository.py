from datetime import datetime, timezone
from uuid import uuid4

from backend.models.dynamodb import db_store
from backend.repositories.base import Repository


class DynamoDBRepository(Repository):

    # ---------- Participants ----------

    def get_vendor(self, vendor_id: str):
        return db_store.get_item(
            f"VENDOR#{vendor_id}",
            "PROFILE"
        )

    def get_ngo(self, ngo_id: str):
        return db_store.get_item(
            f"NGO#{ngo_id}",
            "PROFILE"
        )

    def get_rider(self, rider_id: str):
        return db_store.get_item(
            f"RIDER#{rider_id}",
            "PROFILE"
        )

    def save_vendor(self, vendor_id: str, data: dict):
        item = {
            "PK": f"VENDOR#{vendor_id}",
            "SK": "PROFILE",
            "entity_type": "VENDOR",
            "id": vendor_id,
            **data
        }

        return db_store.put_item(item)

    def save_ngo(self, ngo_id: str, data: dict):
        item = {
            "PK": f"NGO#{ngo_id}",
            "SK": "PROFILE",
            "entity_type": "NGO",
            "id": ngo_id,
            **data
        }

        return db_store.put_item(item)

    def save_rider(self, rider_id: str, data: dict):
        item = {
            "PK": f"RIDER#{rider_id}",
            "SK": "PROFILE",
            "entity_type": "RIDER",
            "id": rider_id,
            **data
        }

        return db_store.put_item(item)

    # ---------- Surplus ----------

    def save_surplus(self, surplus_id: str, data: dict):
        item = {
            "PK": f"SURPLUS#{surplus_id}",
            "SK": "EVENT",
            "entity_type": "SURPLUS",
            "id": surplus_id,
            **data
        }

        return db_store.put_item(item)

    def get_surplus(self, surplus_id: str):
        return db_store.get_item(
            f"SURPLUS#{surplus_id}",
            "EVENT"
        )

    def get_all_surplus(self):
        items = db_store.scan_items()

        return [
            item
            for item in items
            if item.get("entity_type") == "SURPLUS"
        ]

    # ---------- Allocations ----------

    def save_allocation(self, allocation_id: str, data: dict):
        item = {
            "PK": f"ALLOCATION#{allocation_id}",
            "SK": "PLAN",
            "entity_type": "ALLOCATION",
            "id": allocation_id,
            **data
        }

        return db_store.put_item(item)

    def get_allocation(self, allocation_id: str):
        return db_store.get_item(
            f"ALLOCATION#{allocation_id}",
            "PLAN"
        )

    def get_all_allocations(self):
        items = db_store.scan_items()

        return [
            item
            for item in items
            if item.get("entity_type") == "ALLOCATION"
        ]

    # ---------- Events ----------

    def record_event(
        self,
        event_type: str,
        actor: str,
        payload: dict
    ):
        event_id = f"evt_{uuid4().hex[:8]}"
        timestamp = datetime.now(timezone.utc).isoformat()

        item = {
            "PK": f"EVENT#{event_id}",
            "SK": f"TIMESTAMP#{timestamp}",
            "entity_type": "EVENT",
            "event_id": event_id,
            "event_type": event_type,
            "actor": actor,
            "payload": payload,
            "created_at": timestamp
        }

        db_store.put_item(item)

        return item

    def get_events(self):
        items = db_store.scan_items()

        events = [
            item
            for item in items
            if item.get("entity_type") == "EVENT"
        ]

        return sorted(
            events,
            key=lambda event: event["created_at"]
        )

    # ---------- Reset ----------

    def reset(self):
        items = db_store.scan_items()

        for item in items:
            db_store.delete_item(
                item["PK"],
                item.get("SK")
            )