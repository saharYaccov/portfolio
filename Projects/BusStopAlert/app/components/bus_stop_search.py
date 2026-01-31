# app/components/bus_stop_search.py
import streamlit as st
from geopy.geocoders import Nominatim
from typing import Tuple

# יצירת geolocator
geolocator = Nominatim(user_agent="bus_stop_app")

def search_station(name: str) -> Tuple[float,float]:
    """
    Fetch bus stop location by name using OpenStreetMap Nominatim
    """
    location = geolocator.geocode(name , timeout=10)
    if location:
        return location.latitude, location.longitude
    else:
        return None

def bus_stop_search_ui() -> Tuple[float,float]:
    """
    Streamlit UI for searching destination
    """
    query = st.text_input("Enter your destination:", "")
    if query:
        coords = search_station(query)
        if coords:
            st.success(f"Found {query} at {coords[0]:.6f}, {coords[1]:.6f}")
            return coords
        else:
            st.warning("Station not found")
    return None
