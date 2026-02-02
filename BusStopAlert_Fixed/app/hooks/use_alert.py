# app/hooks/use_alert.py
import streamlit as st

def check_alert(time_to_destination_min: float) -> bool:
    """
    Trigger alert if time to destination <= 2 minutes
    Returns True if user pressed "I've arrived"
    """
    if time_to_destination_min <= 2:
        st.warning("🚨 You are about 2 minutes away from your destination!")
        arrived = st.button("I've arrived")
        if arrived:
            return True
    return False
