# app/components/alert.py
import streamlit as st

def show_alert(distance_minutes: float):
    """
    Show alert if user is 2 minutes away
    """
    if distance_minutes <= 2:
        st.warning("🚨 You are about 2 minutes away from your destination!")
        if st.button("I've arrived"):
            return True
    return False
