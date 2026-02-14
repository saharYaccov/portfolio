"""
Target Detection Engine
======================
Automatically identifies the most likely target column(s) in a dataset
using semantic analysis, statistical properties, and machine learning heuristics.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from scipy.stats import entropy
from loguru import logger

from config.settings import target_detection_config


@dataclass
class TargetCandidate:
    """Represents a potential target column"""
    column_name: str
    confidence_score: float
    task_type: str  # 'regression', 'binary_classification', 'multiclass_classification'
    n_unique: int
    data_type: str
    reasoning: List[str]
    
    def __repr__(self):
        return f"TargetCandidate({self.column_name}, {self.confidence_score:.3f}, {self.task_type})"


class TargetDetectionEngine:
    """
    Intelligent target detection system that analyzes datasets
    to automatically identify the most likely target variable(s)
    """
    
    def __init__(self):
        self.config = target_detection_config
        logger.info("Target Detection Engine initialized")
    
    def detect_targets(self, df: pd.DataFrame, 
                      manual_target: Optional[str] = None) -> List[TargetCandidate]:
        """
        Main method to detect target columns
        
        Args:
            df: Input dataframe
            manual_target: Optional manually specified target column
            
        Returns:
            List of TargetCandidate objects ranked by confidence
        """
        logger.info(f"Detecting target columns in dataset with shape {df.shape}")
        
        # If manual target specified, validate and return
        if manual_target:
            if manual_target in df.columns:
                return [self._create_target_from_column(df, manual_target, is_manual=True)]
            else:
                logger.warning(f"Manual target '{manual_target}' not found in columns")
        
        # Detect all potential targets
        candidates = []
        
        for col in df.columns:
            candidate = self._evaluate_column_as_target(df, col)
            if candidate and candidate.confidence_score >= self.config.min_confidence_score:
                candidates.append(candidate)
        
        # Sort by confidence score
        candidates.sort(key=lambda x: x.confidence_score, reverse=True)
        
        # Limit to top candidates
        candidates = candidates[:self.config.max_target_candidates]
        
        logger.info(f"Detected {len(candidates)} target candidates")
        for candidate in candidates:
            logger.info(f"  - {candidate}")
        
        return candidates
    
    def _evaluate_column_as_target(self, df: pd.DataFrame, 
                                   col: str) -> Optional[TargetCandidate]:
        """
        Evaluate a single column as a potential target
        
        Scoring factors:
        1. Semantic matching (column name)
        2. Data type appropriateness
        3. Cardinality analysis
        4. Position in dataframe
        5. Entropy analysis
        6. Correlation with other features
        """
        reasoning = []
        score = 0.0
        
        # Skip if column has all missing values
        if df[col].isna().all():
            return None
        
        # Factor 1: Semantic Analysis (0-0.4 points)
        semantic_score = self._compute_semantic_score(col)
        score += semantic_score
        if semantic_score > 0:
            reasoning.append(f"Column name matches target semantics (+{semantic_score:.2f})")
        
        # Factor 2: Data Type (0-0.2 points)
        dtype_score = self._compute_dtype_score(df[col])
        score += dtype_score
        if dtype_score > 0:
            reasoning.append(f"Appropriate data type (+{dtype_score:.2f})")
        
        # Factor 3: Cardinality (0-0.2 points)
        n_unique = df[col].nunique()
        cardinality_score = self._compute_cardinality_score(df[col], n_unique)
        score += cardinality_score
        if cardinality_score > 0:
            reasoning.append(f"Cardinality suggests target ({n_unique} unique values, +{cardinality_score:.2f})")
        
        # Factor 4: Position Bonus (0-0.2 points)
        if self.config.prefer_last_column and col == df.columns[-1]:
            score += self.config.last_column_bonus
            reasoning.append(f"Last column position bonus (+{self.config.last_column_bonus:.2f})")
        
        # Factor 5: Entropy Analysis (0-0.1 points)
        entropy_score = self._compute_entropy_score(df[col])
        score += entropy_score
        if entropy_score > 0:
            reasoning.append(f"Information entropy suggests target (+{entropy_score:.2f})")
        
        # Determine task type
        task_type = self._determine_task_type(df[col], n_unique)
        data_type = str(df[col].dtype)
        
        # Penalty for poor target characteristics
        if n_unique == len(df):
            score *= 0.3  # Likely an ID column
            reasoning.append("Warning: Unique values equal rows (possible ID)")
        
        if n_unique == 1:
            return None  # Constant column can't be target
        
        return TargetCandidate(
            column_name=col,
            confidence_score=min(score, 1.0),  # Cap at 1.0
            task_type=task_type,
            n_unique=n_unique,
            data_type=data_type,
            reasoning=reasoning
        )
    
    def _compute_semantic_score(self, col_name: str) -> float:
        """
        Compute semantic score based on column name
        Returns 0-0.4
        """
        col_lower = col_name.lower().strip()
        
        # Direct match
        for keyword in self.config.target_keywords:
            if keyword in col_lower:
                if col_lower == keyword:
                    return 0.4  # Exact match
                return 0.3  # Partial match
        
        # Check for common suffixes/prefixes
        target_patterns = ['_target', '_label', '_y', 'target_', 'label_', 'y_']
        for pattern in target_patterns:
            if pattern in col_lower:
                return 0.25
        
        return 0.0
    
    def _compute_dtype_score(self, series: pd.Series) -> float:
        """
        Compute score based on data type appropriateness
        Returns 0-0.2
        """
        dtype = series.dtype
        
        # Numeric types are good for regression
        if pd.api.types.is_numeric_dtype(dtype):
            return 0.2
        
        # Object/category types good for classification
        if pd.api.types.is_object_dtype(dtype) or pd.api.types.is_categorical_dtype(dtype):
            return 0.15
        
        # Boolean is good for binary classification
        if pd.api.types.is_bool_dtype(dtype):
            return 0.2
        
        return 0.05
    
    def _compute_cardinality_score(self, series: pd.Series, n_unique: int) -> float:
        """
        Compute score based on cardinality
        Returns 0-0.2
        """
        n_rows = len(series)
        unique_ratio = n_unique / n_rows
        
        # Binary classification (2 unique values)
        if n_unique == 2:
            return 0.2
        
        # Multiclass classification (3-50 unique values)
        if 3 <= n_unique <= self.config.max_multiclass_values:
            return 0.18
        
        # Regression (many unique values but not all)
        if unique_ratio >= self.config.min_regression_unique_ratio and unique_ratio < 0.9:
            return 0.15
        
        # Too many unique values (likely ID)
        if unique_ratio > 0.95:
            return 0.0
        
        return 0.05
    
    def _compute_entropy_score(self, series: pd.Series) -> float:
        """
        Compute score based on information entropy
        Returns 0-0.1
        
        Target variables often have moderate entropy:
        - Not too uniform (boring)
        - Not too chaotic (ID-like)
        """
        try:
            # Get value counts
            value_counts = series.value_counts(normalize=True)
            
            # Compute Shannon entropy
            ent = entropy(value_counts.values)
            
            # Normalize by maximum possible entropy
            max_entropy = np.log(len(value_counts))
            normalized_entropy = ent / max_entropy if max_entropy > 0 else 0
            
            # Optimal entropy is around 0.3-0.7 (balanced distribution)
            if 0.3 <= normalized_entropy <= 0.7:
                return 0.1
            elif 0.2 <= normalized_entropy <= 0.8:
                return 0.05
            
        except Exception as e:
            logger.debug(f"Entropy computation failed: {e}")
        
        return 0.0
    
    def _determine_task_type(self, series: pd.Series, n_unique: int) -> str:
        """
        Determine the ML task type based on the target column
        """
        dtype = series.dtype
        
        # Binary classification
        if n_unique == 2:
            return 'binary_classification'
        
        # Multiclass classification
        if n_unique <= self.config.max_multiclass_values and \
           (pd.api.types.is_object_dtype(dtype) or 
            pd.api.types.is_categorical_dtype(dtype) or
            pd.api.types.is_bool_dtype(dtype)):
            return 'multiclass_classification'
        
        # Check for numeric regression
        if pd.api.types.is_numeric_dtype(dtype):
            # If many unique values, likely regression
            unique_ratio = n_unique / len(series)
            if unique_ratio >= self.config.min_regression_unique_ratio:
                return 'regression'
            # If few unique values, could be ordinal classification
            elif n_unique <= self.config.max_multiclass_values:
                return 'multiclass_classification'
        
        # Default to regression for numeric, classification for others
        if pd.api.types.is_numeric_dtype(dtype):
            return 'regression'
        else:
            return 'multiclass_classification'
    
    def _create_target_from_column(self, df: pd.DataFrame, col: str, 
                                   is_manual: bool = False) -> TargetCandidate:
        """Create a TargetCandidate from a specified column"""
        n_unique = df[col].nunique()
        task_type = self._determine_task_type(df[col], n_unique)
        
        return TargetCandidate(
            column_name=col,
            confidence_score=1.0 if is_manual else 0.5,
            task_type=task_type,
            n_unique=n_unique,
            data_type=str(df[col].dtype),
            reasoning=["Manually specified target"] if is_manual else ["User selection"]
        )
    
    def get_target_summary(self, candidates: List[TargetCandidate]) -> Dict:
        """
        Generate a summary of detected targets
        """
        if not candidates:
            return {
                'n_candidates': 0,
                'primary_target': None,
                'message': 'No suitable target columns detected'
            }
        
        primary = candidates[0]
        
        return {
            'n_candidates': len(candidates),
            'primary_target': {
                'column': primary.column_name,
                'confidence': primary.confidence_score,
                'task_type': primary.task_type,
                'n_unique': primary.n_unique,
                'reasoning': primary.reasoning
            },
            'secondary_targets': [
                {
                    'column': c.column_name,
                    'confidence': c.confidence_score,
                    'task_type': c.task_type
                }
                for c in candidates[1:]
            ],
            'message': f"Detected {len(candidates)} potential target(s)"
        }


# ================================
# UTILITY FUNCTIONS
# ================================

def detect_datetime_columns(df: pd.DataFrame) -> List[str]:
    """Detect datetime columns in the dataframe"""
    datetime_cols = []
    
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            datetime_cols.append(col)
        else:
            # Try to parse as datetime
            try:
                pd.to_datetime(df[col], errors='raise')
                datetime_cols.append(col)
            except:
                pass
    
    return datetime_cols


def detect_categorical_columns(df: pd.DataFrame, 
                               threshold: int = 50) -> List[str]:
    """
    Detect categorical columns
    
    Args:
        df: Input dataframe
        threshold: Max unique values to consider categorical
    """
    categorical_cols = []
    
    for col in df.columns:
        if pd.api.types.is_categorical_dtype(df[col]) or \
           pd.api.types.is_object_dtype(df[col]):
            if df[col].nunique() <= threshold:
                categorical_cols.append(col)
    
    return categorical_cols
