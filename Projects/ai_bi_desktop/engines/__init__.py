"""
AI BI Desktop - Intelligent Engines
===================================
Core AI engines for automated analysis
"""

from .target_detection import TargetDetectionEngine, TargetCandidate
from .feature_correlation import FeatureCorrelationEngine, FeatureCorrelation
from .graph_selection_old import AutoGraphSelectionEngine, GraphSpec
from .automl import AutoMLEngine, ModelResult
from .insight_generation import InsightGenerationEngine, Insight

__all__ = [
    'TargetDetectionEngine',
    'TargetCandidate',
    'FeatureCorrelationEngine',
    'FeatureCorrelation',
    'AutoGraphSelectionEngine',
    'GraphSpec',
    'AutoMLEngine',
    'ModelResult',
    'InsightGenerationEngine',
    'Insight',
]
