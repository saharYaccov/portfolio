# app/hooks/use_distance.py
import math
from typing import Tuple

def haversine(coord1: Tuple[float,float], coord2: Tuple[float,float]) -> float:
    """
    Calculate distance in km between two GPS points using Haversine formula
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def estimate_time(distance_km: float, speed_kmh: float = 30) -> float:
    """
    Estimate time to destination in minutes
    Default speed: 30 km/h
    """
    return (distance_km / speed_kmh) * 60
