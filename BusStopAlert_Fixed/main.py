import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium
import folium
import requests
from app.hooks.use_distance import haversine, estimate_time
from app.hooks.use_alert import check_alert
from app.components.bus_stop_search import bus_stop_search_ui
from streamlit_autorefresh import st_autorefresh

# --- קונפיג ---
API_URL = "http://127.0.0.1:8000/location"  # Flask API שלך

# --- Streamlit Setup ---
st.set_page_config(page_title="🚌 Bus Stop Alert", layout="wide")
st.title("🚌 Bus Stop Alert")
st.write("Welcome! Enter a destination and start tracking your route. 🚀")

# --- Destination ---
destination_coords = bus_stop_search_ui()
if not destination_coords:
    st.info("Please enter a destination to start tracking.")
    st.stop()
st.success(f"✅ Destination set at: {destination_coords[0]:.6f}, {destination_coords[1]:.6f}")

# --- עדכון אוטומטי כל 15 שניות ---
st_autorefresh(interval=15000, limit=None, key="gps_refresh")  # 15 שניות

# --- פונקציה לקבלת מיקום מהשרת Flask ---
def get_latest_coords():
    try:
        res = requests.get("http://127.0.0.1:8000/location/latest", timeout=3)
        res.raise_for_status()
        data = res.json()
        print(f"Received data: {data}")
        # בדיקה אם יש מיקום אמיתי
        if "lat" in data and "lon" in data and data["lat"] is not None and data["lon"] is not None:
            return (data["lat"], data["lon"])
    except Exception as e:
        print(f"Error fetching location: {e}")
        st.warning(f"Could not fetch latest coordinates: {e}")
    # fallback Tel Aviv
    return (32.0853, 34.7818)

user_coords = get_latest_coords()
st.success(f"📍 Your current location (GPS-based): {user_coords[0]:.6f}, {user_coords[1]:.6f}")

# כפתור לשליחת מיקום נוכחי
st.subheader("📡 Update Your Location")
components.html("""
<div style="text-align: center; padding: 20px;">
    <button 
        id="sendLocationBtn"
        style="
            background-color: #4CAF50;
            color: white;
            padding: 15px 32px;
            text-align: center;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        "
        onclick="sendLocation()">
        📍 Send My Location
    </button>
    <div id="status" style="margin-top: 15px; font-weight: bold;"></div>
</div>

<script>
function sendLocation() {
    const statusDiv = document.getElementById('status');
    const btn = document.getElementById('sendLocationBtn');
    
    statusDiv.innerHTML = '⏳ Getting your location...';
    statusDiv.style.color = 'orange';
    btn.disabled = true;
    
    if (!navigator.geolocation) {
        statusDiv.innerHTML = '❌ Geolocation not supported';
        statusDiv.style.color = 'red';
        btn.disabled = false;
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            fetch('http://127.0.0.1:8000/location', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({lat: lat, lon: lon})
            })
            .then(response => response.json())
            .then(data => {
                statusDiv.innerHTML = '✅ Location sent successfully! Lat: ' + lat.toFixed(6) + ', Lon: ' + lon.toFixed(6);
                statusDiv.style.color = 'green';
                btn.disabled = false;
                // רענון הדף אחרי 2 שניות
                setTimeout(() => {
                    window.parent.location.reload();
                }, 2000);
            })
            .catch(error => {
                statusDiv.innerHTML = '❌ Failed to send location: ' + error;
                statusDiv.style.color = 'red';
                btn.disabled = false;
            });
        },
        function(error) {
            statusDiv.innerHTML = '❌ Error: ' + error.message;
            statusDiv.style.color = 'red';
            btn.disabled = false;
        }
    );
}
</script>
""", height=150)

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
if check_alert(time_min):
    st.balloons()
    st.success("🎉 Congratulations! You have arrived at your destination.")
else:
    st.info("Tracking in progress... Keep moving towards your destination! 🚶‍♂️🚌")
