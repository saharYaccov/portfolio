# app/components/map_view.py
import streamlit as st
import folium
from streamlit_folium import st_folium
from typing import Tuple

def show_map(user_location: Tuple[float,float], destination: Tuple[float,float]):
    """
    Displays the map with user's current location and destination
    """
    m = folium.Map(location=user_location, zoom_start=13)

    # User location marker
    folium.Marker(
        location=user_location,
        popup="You are here",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Destination marker
    folium.Marker(
        location=destination,
        popup="Destination",
        icon=folium.Icon(color="red")
    ).add_to(m)

    # Line between current location and destination
    folium.PolyLine([user_location, destination], color="green").add_to(m)

    st_folium(m, width=700, height=500)
