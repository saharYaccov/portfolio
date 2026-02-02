# app/utils/haversine.py
import math
from typing import Tuple

def haversine(coord1: Tuple[float,float], coord2: Tuple[float,float]) -> float:
    """
    Calculate distance in kilometers between two GPS coordinates using Haversine formula
    coord1, coord2: (lat, lon)
    Returns distance in km
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth's radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    return distance
