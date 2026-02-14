# AI BI Desktop Application - Configuration
# This file contains all system-wide configuration parameters

import os
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseModel, Field

# ================================
# PROJECT PATHS
# ================================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
CACHE_DIR = PROJECT_ROOT / "cache"
LOGS_DIR = PROJECT_ROOT / "logs"
LEARNING_DIR = PROJECT_ROOT / "learning"  # For adaptive learning

# Create directories
for dir_path in [DATA_DIR, MODELS_DIR, CACHE_DIR, LOGS_DIR, LEARNING_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


# ================================
# APPLICATION SETTINGS
# ================================
class AppConfig(BaseModel):
    """Main application configuration"""
    
    # Application metadata
    app_name: str = "AI BI Desktop Assistant"
    version: str = "1.0.0"
    
    # Background service
    enable_background_service: bool = True
    tray_icon_enabled: bool = True
    
    # Resource limits
    max_memory_mb: int = 2048
    max_cpu_percent: float = 50.0
    
    # File monitoring
    watch_downloads_folder: bool = True
    auto_analyze_threshold_mb: float = 100.0
    
    # Gradio settings
    gradio_port: int = 7860
    gradio_share: bool = False
    gradio_auth: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_rotation: str = "10 MB"
    log_retention: str = "7 days"


# ================================
# DATA PROCESSING SETTINGS
# ================================
class DataConfig(BaseModel):
    """Data processing configuration"""
    
    # File limits
    max_file_size_mb: float = 500.0
    max_rows: int = 1_000_000
    max_columns: int = 1000
    
    # Missing data handling
    missing_threshold: float = 0.5  # Drop columns with >50% missing
    
    # Data type detection
    categorical_threshold: int = 50  # Unique values threshold
    datetime_detection: bool = True
    
    # Sampling for large datasets
    enable_sampling: bool = True
    sample_size: int = 100_000
    stratified_sampling: bool = True


# ================================
# TARGET DETECTION SETTINGS
# ================================
class TargetDetectionConfig(BaseModel):
    """Target detection configuration"""
    
    # Semantic keywords (case-insensitive)
    target_keywords: list = [
        'target', 'label', 'y', 'outcome', 'result', 
        'prediction', 'class', 'output', 'response',
        'churn', 'fraud', 'default', 'conversion',
        'price', 'sales', 'revenue', 'value'
    ]
    
    # Detection thresholds
    min_confidence_score: float = 0.3
    max_target_candidates: int = 3
    
    # Column position bias
    prefer_last_column: bool = True
    last_column_bonus: float = 0.2
    
    # Cardinality rules
    binary_classification_values: int = 2
    max_multiclass_values: int = 50
    min_regression_unique_ratio: float = 0.05


# ================================
# FEATURE ANALYSIS SETTINGS
# ================================
class FeatureAnalysisConfig(BaseModel):
    """Feature correlation and statistical analysis configuration"""
    
    # Correlation thresholds
    min_correlation: float = 0.1
    strong_correlation: float = 0.5
    very_strong_correlation: float = 0.7
    
    # Statistical significance
    p_value_threshold: float = 0.05
    
    # Feature selection
    max_features_to_display: int = 20
    top_features_for_graphs: int = 10
    
    # Statistical tests
    use_pearson: bool = True
    use_spearman: bool = True
    use_anova: bool = True
    use_chi_square: bool = True
    use_point_biserial: bool = True


# ================================
# AUTO GRAPH SELECTION SETTINGS
# ================================
class GraphSelectionConfig(BaseModel):
    """Automatic graph selection configuration"""
    
    # Graph priorities
    graph_types: Dict[str, int] = {
        'scatter': 1,
        'box': 2,
        'violin': 3,
        'bar': 4,
        'heatmap': 5,
        'histogram': 6,
        'line': 7,
        'density': 8
    }
    
    # Visualization limits
    max_graphs_per_page: int = 12
    max_categories_in_bar: int = 20
    max_points_in_scatter: int = 10000
    
    # Plotly configuration
    plotly_theme: str = "plotly_white"
    enable_interactive: bool = True
    show_grid: bool = True


# ================================
# AUTOML SETTINGS
# ================================
class AutoMLConfig(BaseModel):
    """AutoML and model training configuration"""
    
    # Optuna optimization
    n_trials: int = 50
    optimization_timeout_seconds: int = 300
    n_jobs: int = -1
    
    # Cross-validation
    cv_folds: int = 5
    stratified_cv: bool = True
    
    # Model selection
    models_to_try: list = [
        'random_forest',
        'catboost',
        'lightgbm',
        'xgboost',
        'logistic_regression',
        'linear_regression',
        'ridge',
        'gradient_boosting'
    ]
    
    # Preprocessing
    handle_missing: bool = True
    encode_categoricals: bool = True
    scale_features: bool = True
    feature_selection: bool = True
    
    # Feature selection
    max_features_ratio: float = 0.8
    feature_importance_threshold: float = 0.01
    
    # Early stopping
    enable_early_stopping: bool = True
    early_stopping_rounds: int = 10
    
    # Ensemble methods
    enable_stacking: bool = False
    enable_voting: bool = False


# ================================
# MODEL EVALUATION SETTINGS
# ================================
class EvaluationConfig(BaseModel):
    """Model evaluation metrics configuration"""
    
    # Classification metrics
    classification_metrics: list = [
        'accuracy',
        'precision',
        'recall',
        'f1',
        'roc_auc',
        'log_loss'
    ]
    
    # Regression metrics
    regression_metrics: list = [
        'r2',
        'mae',
        'rmse',
        'mape',
        'mse'
    ]
    
    # Display configuration
    metrics_decimal_places: int = 4
    show_confidence_intervals: bool = True


# ================================
# EXPLAINABILITY SETTINGS
# ================================
class ExplainabilityConfig(BaseModel):
    """Model explainability configuration"""
    
    # SHAP configuration
    enable_shap: bool = True
    shap_max_samples: int = 1000
    shap_method: str = "auto"  # auto, tree, kernel, linear
    
    # Feature importance
    top_features_to_explain: int = 15
    
    # Partial dependence
    enable_pdp: bool = True
    pdp_features: int = 5


# ================================
# INSIGHT GENERATION SETTINGS
# ================================
class InsightConfig(BaseModel):
    """AI insight generation configuration"""
    
    # Insight generation
    min_insight_length: int = 100
    max_insight_length: int = 500
    
    # Insight components
    include_correlation_insights: bool = True
    include_model_insights: bool = True
    include_feature_importance: bool = True
    include_business_context: bool = True
    
    # Language settings
    language: str = "en"
    professional_tone: bool = True
    avoid_technical_jargon: bool = False


# ================================
# ADAPTIVE LEARNING SETTINGS
# ================================
class LearningConfig(BaseModel):
    """Adaptive learning system configuration"""
    
    # Learning mechanisms
    enable_learning: bool = True
    learning_rate: float = 0.1
    
    # History tracking
    max_history_entries: int = 1000
    track_model_performance: bool = True
    track_graph_interactions: bool = True
    track_user_preferences: bool = True
    
    # Adaptation
    adapt_model_selection: bool = True
    adapt_graph_selection: bool = True
    adapt_feature_selection: bool = True


# ================================
# INSTANTIATE CONFIGURATIONS
# ================================
app_config = AppConfig()
data_config = DataConfig()
target_detection_config = TargetDetectionConfig()
feature_analysis_config = FeatureAnalysisConfig()
graph_selection_config = GraphSelectionConfig()
automl_config = AutoMLConfig()
evaluation_config = EvaluationConfig()
explainability_config = ExplainabilityConfig()
insight_config = InsightConfig()
learning_config = LearningConfig()
