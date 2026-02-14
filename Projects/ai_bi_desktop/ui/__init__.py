"""
AI BI Desktop - User Interface
==============================
Gradio-based dashboard interface
"""

from .gradio_app import GradioDashboard, launch_dashboard

__all__ = [
    'GradioDashboard',
    'launch_dashboard',
]
