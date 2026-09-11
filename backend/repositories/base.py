from abc import ABC, abstractmethod


class Repository(ABC):

    # ---------- Participants ----------

    @abstractmethod
    def get_vendor(self, vendor_id: str):
        pass

    @abstractmethod
    def get_ngo(self, ngo_id: str):
        pass

    @abstractmethod
    def get_rider(self, rider_id: str):
        pass

    @abstractmethod
    def save_vendor(self, vendor_id: str, data: dict):
        pass

    @abstractmethod
    def save_ngo(self, ngo_id: str, data: dict):
        pass

    @abstractmethod
    def save_rider(self, rider_id: str, data: dict):
        pass

    # ---------- Surplus ----------

    @abstractmethod
    def save_surplus(self, surplus_id: str, data: dict):
        pass

    @abstractmethod
    def get_surplus(self, surplus_id: str):
        pass

    @abstractmethod
    def get_all_surplus(self):
        pass

    # ---------- Allocations ----------

    @abstractmethod
    def save_allocation(self, allocation_id: str, data: dict):
        pass

    @abstractmethod
    def get_allocation(self, allocation_id: str):
        pass

    @abstractmethod
    def get_all_allocations(self):
        pass

    # ---------- Events ----------

    @abstractmethod
    def record_event(
        self,
        event_type: str,
        actor: str,
        payload: dict
    ):
        pass

    @abstractmethod
    def get_events(self):
        pass

    # ---------- Reset ----------

    @abstractmethod
    def reset(self):
        pass