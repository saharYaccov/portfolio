import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
from app.hooks.use_distance import haversine, estimate_time
from app.hooks.use_alert import check_alert
from app.components.bus_stop_search import bus_stop_search_ui
from streamlit_autorefresh import st_autorefresh

# --- קונפיג ---
IP_GEO_URL = "http://ip-api.com/json"
API_URL = "http://127.0.0.1:8000/location"  # אפשר לשלוח לשרת

# --- Streamlit Setup ---
st.set_page_config(page_title="🚌 Bus Stop Alert", layout="wide")
st.title("🚌 Bus Stop Alert")
st.write("Welcome! Enter a destination and start tracking your route. 🚀")

# --- Destination ---
destination_coords = bus_stop_search_ui()
if not destination_coords:
    st.info("Please enter a destination to start tracking.")
    st.stop()
else:
    st.success(f"✅ Destination set at: {destination_coords[0]:.6f}, {destination_coords[1]:.6f}")

# --- עדכון אוטומטי כל 15 שניות ---
st_autorefresh(interval=15000, limit=None, key="gps_refresh")  # 15,000ms = 15 שניות

# --- פונקציה לקבלת מיקום לפי IP ---
def get_location_from_ip():
    try:
        res = requests.get(IP_GEO_URL, timeout=5)
        data = res.json()
        if data.get("status") == "success":
            lat, lon = data["lat"], data["lon"]
            # אפשר לשלוח לשרת
            try:
                requests.post(API_URL, json={"lat": lat, "lon": lon}, timeout=3)
            except:
                pass
            return (lat, lon)
    except:
        pass
    # fallback Tel Aviv אם נכשל
    return (32.0853, 34.7818)

# --- קבלת מיקום נוכחי ---
user_coords = get_location_from_ip()
st.success(f"📍 Your current location (IP-based): {user_coords[0]:.6f}, {user_coords[1]:.6f}")

# --- Map ---
m = folium.Map(location=user_coords, zoom_start=13)
folium.Marker(user_coords, tooltip="You are here", icon=folium.Icon(color="blue")).add_to(m)
folium.Marker(destination_coords, tooltip="Destination", icon=folium.Icon(color="red")).add_to(m)
folium.PolyLine([user_coords, destination_coords], color="green", weight=3, opacity=0.7).add_to(m)
st_folium(m, width=700, height=500)

# --- Distance & Time ---
distance_km = haversine(user_coords, destination_coords)
st.metric("Distance to destination", f"{distance_km:.2f} km")

speed_kmh = st.number_input("Estimated speed (km/h)", value=30.0, min_value=1.0)
time_min = estimate_time(distance_km, speed_kmh)
st.metric("Estimated travel time", f"{time_min:.1f} min")

# --- Alert ---
arrived = check_alert(time_min)
if arrived:
    st.balloons()
    st.success("🎉 Congratulations! You have arrived at your destination.")
else:
    st.info("Tracking in progress... Keep moving towards your destination! 🚶‍♂️🚌")
