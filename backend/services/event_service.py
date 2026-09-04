from datetime import datetime

class StateDB:
    def __init__(self):
        self.vendors = {
            "vendor_1": {"name": "Restaurant A", "location": {"lat": 28.61, "lng": 77.23}, "trust_score": 0.95},
            "vendor_2": {"name": "Canteen B", "location": {"lat": 28.62, "lng": 77.21}, "trust_score": 0.88}
        }
        self.ngos = {
            "ngo_1": {"name": "Shelter X", "location": {"lat": 28.63, "lng": 77.22}, "capacity": 50, "current_capacity": 20, "trust_score": 0.94},
            "ngo_2": {"name": "Food Bank Y", "location": {"lat": 28.60, "lng": 77.25}, "capacity": 100, "current_capacity": 80, "trust_score": 0.90}
        }
        self.riders = {
            "rider_1": {"name": "Rider John", "location": {"lat": 28.615, "lng": 77.225}, "available": True},
            "rider_2": {"name": "Rider Sarah", "location": {"lat": 28.605, "lng": 77.245}, "available": True}
        }
        self.surplus = []
        self.plans = []
        self.timeline = []

    def add_timeline_event(self, agent: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.timeline.append({"timestamp": timestamp, "agent": agent, "message": message})
        print(f"[{timestamp}] {agent}: {message}")

    def reset(self):
        self.surplus = []
        self.plans = []
        self.timeline = []
        for r in self.riders.values():
            r["available"] = True
        self.ngos["ngo_1"]["current_capacity"] = 20
        self.ngos["ngo_2"]["current_capacity"] = 80

state_db = StateDB()
