import requests
import threading
import time

API_URL = "http://127.0.0.1:8000/location"
IP_GEO_URL = "http://ip-api.com/json"

class GPSHandler:
    def __init__(self, update_interval=10):
        self.last_location = None
        self.update_interval = update_interval  # שניות
        self._updating = False

    # --- מקבל את הקואורדינטות הנוכחיות ---
    def get_location(self):
        if self.last_location:
            return self.last_location
        try:
            res = requests.get(IP_GEO_URL, timeout=5)
            data = res.json()
            if data.get("status") == "success":
                lat, lon = data["lat"], data["lon"]
                self.last_location = (lat, lon)
                self.send_location(lat, lon)
                return self.last_location
        except Exception:
            pass
        return None

    # --- מדפיס את הקואורדינטות ---
    def print_location(self):
        if self.last_location:
            print(f"[GPS] Latitude: {self.last_location[0]:.6f}, Longitude: {self.last_location[1]:.6f}")
        else:
            print("[GPS] Location not available.")

    # --- שולח לשרת ---
    def send_location(self, lat, lon):
        try:
            requests.post(API_URL, json={"lat": lat, "lon": lon}, timeout=5)
        except Exception:
            pass

    # --- עדכון GPS אוטומטי כל X שניות ---
    def update_gps(self):
        self._updating = True
        def _update():
            if not self._updating:
                return
            self.get_location()
            self.print_location()
            # קריאה מחודשת אחרי self.update_interval שניות
            threading.Timer(self.update_interval, _update).start()
        _update()

    # --- עצירת עדכון אוטומטי ---
    def stop_update(self):
        self._updating = False
