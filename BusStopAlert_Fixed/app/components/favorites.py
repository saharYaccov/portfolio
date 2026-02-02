# app/components/favorites.py
import streamlit as st

def load_favorites():
    return st.session_state.get("favorites", [])

def add_favorite(station_name: str):
    if "favorites" not in st.session_state:
        st.session_state["favorites"] = []
    if station_name not in st.session_state["favorites"]:
        st.session_state["favorites"].append(station_name)

def remove_favorite(station_name: str):
    if "favorites" in st.session_state and station_name in st.session_state["favorites"]:
        st.session_state["favorites"].remove(station_name)

def favorites_ui():
    favorites = load_favorites()
    st.subheader("Favorites")
    for fav in favorites:
        st.write(f"- {fav}")
