"""
AI BI Desktop - Core Components
===============================
Core orchestration and background services
"""

from .orchestrator import AIOrchestrator, AnalysisResult, quick_analyze

__all__ = [
    'AIOrchestrator',
    'AnalysisResult',
    'quick_analyze',
]
