from plyer import gps
import requests
import threading
import time

API_URL = "http://127.0.0.1:8000/location"
IP_GEO_URL = "http://ip-api.com/json"

class GPSHandler:
    def __init__(self, update_interval=10):
        self.last_location = None
        self.update_interval = update_interval
        self._updating = False

        # קונפיגורציה של Plyer GPS
        try:
            gps.configure(on_location=self._on_gps_location)
            gps.start()
        except NotImplementedError:
            print("GPS not supported on this device, falling back to IP-based location")

    # --- פונקציה פנימית לקבלת GPS מהמכשיר ---
    def _on_gps_location(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        if lat and lon:
            self.last_location = (lat, lon)
            self.send_location(lat, lon)
            self.print_location()

    # --- מקבל מיקום (GPS קודם, אחרת GeoIP) ---
    def get_location(self):
        if self.last_location:
            return self.last_location
        # fallback ל-GeoIP
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

    # --- מדפיס מיקום ---
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

    # --- עדכון אוטומטי כל X שניות ---
    def update_gps(self):
        self._updating = True
        def _update():
            if not self._updating:
                return
            self.get_location()
            self.print_location()
            threading.Timer(self.update_interval, _update).start()
        _update()

    # --- עצירה ---
    def stop_update(self):
        self._updating = False

# --- שימוש ---
handler = GPSHandler(update_interval=15)
handler.update_gps()

# להריץ זמן מה
time.sleep(10)
handler.stop_update()
