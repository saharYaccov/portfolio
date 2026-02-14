"""
AI Orchestrator
===============
Main orchestration system that coordinates all AI engines
and manages the complete analysis workflow.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import joblib
from loguru import logger

from config.settings import (
    data_config, MODELS_DIR, CACHE_DIR, LEARNING_DIR
)
from engines.target_detection import TargetDetectionEngine, TargetCandidate
from engines.feature_correlation import FeatureCorrelationEngine, FeatureCorrelation
from engines.graph_selection import AutoGraphSelectionEngine, GraphSpec
from engines.automl import AutoMLEngine, ModelResult
from engines.insight_generation import InsightGenerationEngine, Insight


@dataclass
class AnalysisResult:
    """Complete analysis results"""
    dataset_info: Dict[str, Any]
    target_candidates: List[TargetCandidate]
    selected_target: TargetCandidate
    correlations: List[FeatureCorrelation]
    graph_specs: List[GraphSpec]
    best_model: ModelResult
    all_models: List[ModelResult]
    insights: List[Insight]
    feature_importance_df: Optional[pd.DataFrame]
    
    def __repr__(self):
        return f"AnalysisResult(target={self.selected_target.column_name}, " \
               f"model={self.best_model.model_name})"


class AIOrchestrator:
    """
    Central orchestrator that coordinates all AI engines
    to perform complete automated analysis
    """
    
    def __init__(self):
        logger.info("Initializing AI Orchestrator...")
        
        # Initialize all engines
        self.target_engine = TargetDetectionEngine()
        self.correlation_engine = FeatureCorrelationEngine()
        self.graph_engine = AutoGraphSelectionEngine()
        self.automl_engine = AutoMLEngine()
        self.insight_engine = InsightGenerationEngine()
        
        self.config = data_config
        
        logger.info("AI Orchestrator initialized successfully")
    
    def analyze_dataset(self,
                       file_path: str,
                       manual_target: Optional[str] = None) -> AnalysisResult:
        """
        Main method to perform complete automated analysis
        
        Args:
            file_path: Path to CSV or Excel file
            manual_target: Optional manually specified target column
            
        Returns:
            AnalysisResult containing all analysis outputs
        """
        logger.info(f"Starting analysis of {file_path}")
        
        # Step 1: Load Data
        df = self._load_data(file_path)
        logger.info(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Step 2: Data Profiling
        dataset_info = self._profile_dataset(df)
        
        # Step 3: Target Detection
        logger.info("Step 1/5: Detecting target column...")
        target_candidates = self.target_engine.detect_targets(df, manual_target)
        
        if not target_candidates:
            raise ValueError("No suitable target column detected. Please specify manually.")
        
        selected_target = target_candidates[0]
        logger.info(f"Selected target: {selected_target.column_name} ({selected_target.task_type})")
        
        # Step 4: Feature Correlation Analysis
        logger.info("Step 2/5: Analyzing feature correlations...")
        correlations = self.correlation_engine.analyze_correlations(
            df,
            selected_target.column_name,
            selected_target.task_type
        )
        logger.info(f"Found {len(correlations)} significant correlations")
        
        # Step 5: Auto Graph Selection
        logger.info("Step 3/5: Selecting optimal visualizations...")
        graph_specs = self.graph_engine.select_graphs(
            df,
            selected_target.column_name,
            selected_target.task_type,
            correlations
        )
        logger.info(f"Generated {len(graph_specs)} graph specifications")
        
        # Step 6: AutoML Training
        logger.info("Step 4/5: Training and optimizing ML models...")
        best_model, all_models = self.automl_engine.auto_train(
            df,
            selected_target.column_name,
            selected_target.task_type
        )
        logger.info(f"Best model: {best_model.model_name} (CV: {best_model.mean_cv_score:.4f})")
        
        # Step 7: Insight Generation
        logger.info("Step 5/5: Generating AI insights...")
        insights = self.insight_engine.generate_all_insights(
            df,
            selected_target.column_name,
            selected_target.task_type,
            correlations,
            best_model,
            all_models,
            graph_specs
        )
        logger.info(f"Generated {len(insights)} insights")
        
        # Compile results
        result = AnalysisResult(
            dataset_info=dataset_info,
            target_candidates=target_candidates,
            selected_target=selected_target,
            correlations=correlations,
            graph_specs=graph_specs,
            best_model=best_model,
            all_models=all_models,
            insights=insights,
            feature_importance_df=best_model.feature_importance
        )
        
        # Save result
        self._save_analysis_result(result, file_path)
        
        logger.info("Analysis complete!")
        
        return result
    
    def _load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from CSV or Excel file
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.config.max_file_size_mb:
            raise ValueError(f"File too large: {file_size_mb:.1f} MB (max: {self.config.max_file_size_mb} MB)")
        
        # Load based on extension
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Validate dataset size
        if len(df) > self.config.max_rows:
            logger.warning(f"Dataset has {len(df)} rows, sampling to {self.config.max_rows}")
            df = df.sample(n=self.config.max_rows, random_state=42)
        
        if len(df.columns) > self.config.max_columns:
            raise ValueError(f"Too many columns: {len(df.columns)} (max: {self.config.max_columns})")
        
        # Drop columns with too many missing values
        missing_threshold = self.config.missing_threshold
        cols_to_drop = [
            col for col in df.columns 
            if df[col].isna().mean() > missing_threshold
        ]
        
        if cols_to_drop:
            logger.info(f"Dropping {len(cols_to_drop)} columns with >{missing_threshold*100}% missing data")
            df = df.drop(columns=cols_to_drop)
        
        return df
    
    def _profile_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate dataset profile/statistics
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        profile = {
            'n_rows': len(df),
            'n_columns': len(df.columns),
            'n_numeric': len(numeric_cols),
            'n_categorical': len(categorical_cols),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'missing_data': {
                col: df[col].isna().sum() / len(df) * 100
                for col in df.columns if df[col].isna().any()
            },
            'column_types': {
                col: str(df[col].dtype) for col in df.columns
            }
        }
        
        return profile
    
    def _save_analysis_result(self, result: AnalysisResult, file_path: str):
        """
        Save analysis result for future reference
        """
        try:
            file_name = Path(file_path).stem
            save_path = CACHE_DIR / f"{file_name}_analysis.pkl"
            
            joblib.dump(result, save_path)
            logger.info(f"Analysis result saved to {save_path}")
            
        except Exception as e:
            logger.warning(f"Failed to save analysis result: {e}")
    
    def load_analysis_result(self, file_path: str) -> Optional[AnalysisResult]:
        """
        Load previously saved analysis result
        """
        try:
            file_name = Path(file_path).stem
            load_path = CACHE_DIR / f"{file_name}_analysis.pkl"
            
            if load_path.exists():
                result = joblib.load(load_path)
                logger.info(f"Loaded cached analysis from {load_path}")
                return result
            
        except Exception as e:
            logger.warning(f"Failed to load cached analysis: {e}")
        
        return None


# ================================
# QUICK ANALYSIS FUNCTION
# ================================

def quick_analyze(file_path: str, 
                 target_col: Optional[str] = None) -> AnalysisResult:
    """
    Quick analysis function for easy usage
    
    Example:
        result = quick_analyze('data.csv')
        result = quick_analyze('data.xlsx', target_col='price')
    """
    orchestrator = AIOrchestrator()
    return orchestrator.analyze_dataset(file_path, target_col)
