"""
Feature Correlation Engine
==========================
Analyzes correlations and statistical relationships between features and targets.
Automatically selects appropriate statistical tests based on data types.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from scipy import stats
from scipy.stats import pearsonr, spearmanr, pointbiserialr, chi2_contingency, f_oneway
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from loguru import logger

from config.settings import feature_analysis_config


@dataclass
class FeatureCorrelation:
    """Represents correlation between a feature and target"""
    feature_name: str
    target_name: str
    correlation_value: float
    p_value: float
    test_type: str
    significance: str  # 'highly_significant', 'significant', 'not_significant'
    relationship_strength: str  # 'very_strong', 'strong', 'moderate', 'weak'
    feature_type: str  # 'numeric', 'categorical', 'datetime'
    
    def __repr__(self):
        return f"FeatureCorrelation({self.feature_name} -> {self.target_name}: " \
               f"{self.correlation_value:.3f}, p={self.p_value:.4f}, {self.test_type})"


class FeatureCorrelationEngine:
    """
    Intelligent correlation analysis system that automatically selects
    the most appropriate statistical tests based on data types
    """
    
    def __init__(self):
        self.config = feature_analysis_config
        logger.info("Feature Correlation Engine initialized")
    
    def analyze_correlations(self, 
                            df: pd.DataFrame,
                            target_col: str,
                            task_type: str) -> List[FeatureCorrelation]:
        """
        Main method to analyze all feature-target correlations
        
        Args:
            df: Input dataframe
            target_col: Name of target column
            task_type: 'regression', 'binary_classification', 'multiclass_classification'
            
        Returns:
            List of FeatureCorrelation objects ranked by strength
        """
        logger.info(f"Analyzing correlations for target: {target_col} ({task_type})")
        
        # Get features (all columns except target)
        feature_cols = [col for col in df.columns if col != target_col]
        
        correlations = []
        
        for feature in feature_cols:
            try:
                corr = self._compute_correlation(df, feature, target_col, task_type)
                if corr and abs(corr.correlation_value) >= self.config.min_correlation:
                    correlations.append(corr)
            except Exception as e:
                logger.warning(f"Failed to compute correlation for {feature}: {e}")
        
        # Sort by absolute correlation value
        correlations.sort(key=lambda x: abs(x.correlation_value), reverse=True)
        
        # Limit to top features
        correlations = correlations[:self.config.max_features_to_display]
        
        logger.info(f"Found {len(correlations)} significant correlations")
        
        return correlations
    
    def _compute_correlation(self,
                            df: pd.DataFrame,
                            feature: str,
                            target: str,
                            task_type: str) -> Optional[FeatureCorrelation]:
        """
        Compute correlation using the most appropriate statistical test
        """
        # Determine feature and target types
        feature_type = self._get_column_type(df[feature])
        target_type = self._get_column_type(df[target])
        
        # Remove missing values
        valid_mask = df[[feature, target]].notna().all(axis=1)
        feature_data = df.loc[valid_mask, feature]
        target_data = df.loc[valid_mask, target]
        
        if len(feature_data) < 10:  # Not enough data
            return None
        
        # Select appropriate test
        correlation_value, p_value, test_type = self._select_and_compute_test(
            feature_data, target_data, feature_type, target_type, task_type
        )
        
        if correlation_value is None:
            return None
        
        # Determine significance
        significance = self._determine_significance(p_value)
        
        # Determine relationship strength
        relationship_strength = self._determine_strength(abs(correlation_value))
        
        return FeatureCorrelation(
            feature_name=feature,
            target_name=target,
            correlation_value=correlation_value,
            p_value=p_value,
            test_type=test_type,
            significance=significance,
            relationship_strength=relationship_strength,
            feature_type=feature_type
        )
    
    def _select_and_compute_test(self,
                                 feature_data: pd.Series,
                                 target_data: pd.Series,
                                 feature_type: str,
                                 target_type: str,
                                 task_type: str) -> Tuple[Optional[float], Optional[float], str]:
        """
        Select and compute the most appropriate statistical test
        
        Returns:
            (correlation_value, p_value, test_name)
        """
        
        # CASE 1: Both numeric (Regression or numeric target)
        if feature_type == 'numeric' and target_type == 'numeric':
            # Try Pearson first (assumes linear relationship)
            if self.config.use_pearson:
                try:
                    corr, p_val = pearsonr(feature_data, target_data)
                    return corr, p_val, "Pearson"
                except:
                    pass
            
            # Fallback to Spearman (non-parametric, handles monotonic relationships)
            if self.config.use_spearman:
                try:
                    corr, p_val = spearmanr(feature_data, target_data)
                    return corr, p_val, "Spearman"
                except:
                    pass
        
        # CASE 2: Numeric feature, binary categorical target
        elif feature_type == 'numeric' and target_type == 'categorical':
            if target_data.nunique() == 2 and self.config.use_point_biserial:
                # Point-biserial correlation
                try:
                    # Encode binary target as 0/1
                    target_binary = pd.factorize(target_data)[0]
                    corr, p_val = pointbiserialr(target_binary, feature_data)
                    return corr, p_val, "Point-Biserial"
                except:
                    pass
            
            # ANOVA for multiclass
            if self.config.use_anova:
                try:
                    groups = [feature_data[target_data == cat].values 
                             for cat in target_data.unique()]
                    f_stat, p_val = f_oneway(*groups)
                    
                    # Convert F-statistic to pseudo-correlation (eta-squared)
                    # η² = SS_between / SS_total
                    # For simplicity, use normalized F-stat as correlation proxy
                    eta_squared = f_stat / (f_stat + len(feature_data) - len(groups))
                    corr = np.sqrt(eta_squared) if eta_squared >= 0 else 0
                    
                    return corr, p_val, "ANOVA"
                except:
                    pass
        
        # CASE 3: Categorical feature, numeric target (same as CASE 2, reversed)
        elif feature_type == 'categorical' and target_type == 'numeric':
            if self.config.use_anova:
                try:
                    groups = [target_data[feature_data == cat].values 
                             for cat in feature_data.unique()]
                    f_stat, p_val = f_oneway(*groups)
                    
                    eta_squared = f_stat / (f_stat + len(target_data) - len(groups))
                    corr = np.sqrt(eta_squared) if eta_squared >= 0 else 0
                    
                    return corr, p_val, "ANOVA"
                except:
                    pass
        
        # CASE 4: Both categorical
        elif feature_type == 'categorical' and target_type == 'categorical':
            if self.config.use_chi_square:
                try:
                    # Create contingency table
                    contingency = pd.crosstab(feature_data, target_data)
                    chi2, p_val, dof, expected = chi2_contingency(contingency)
                    
                    # Cramér's V as correlation measure
                    n = len(feature_data)
                    min_dim = min(contingency.shape[0] - 1, contingency.shape[1] - 1)
                    cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
                    
                    return cramers_v, p_val, "Chi-Square (Cramér's V)"
                except:
                    pass
        
        # FALLBACK: Mutual Information (works for any combination)
        try:
            # Encode categorical variables
            if feature_type == 'categorical':
                feature_encoded = pd.factorize(feature_data)[0].reshape(-1, 1)
            else:
                feature_encoded = feature_data.values.reshape(-1, 1)
            
            if target_type == 'categorical' or task_type != 'regression':
                target_encoded = pd.factorize(target_data)[0]
                mi = mutual_info_classif(feature_encoded, target_encoded, 
                                        random_state=42)[0]
            else:
                mi = mutual_info_regression(feature_encoded, target_data.values,
                                           random_state=42)[0]
            
            # Normalize MI to [0, 1] range (approximate)
            mi_normalized = min(mi / 2.0, 1.0)
            
            return mi_normalized, 0.001, "Mutual Information"
        except Exception as e:
            logger.warning(f"All correlation methods failed: {e}")
            return None, None, "None"
    
    def _get_column_type(self, series: pd.Series) -> str:
        """Determine if column is numeric, categorical, or datetime"""
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'datetime'
        elif pd.api.types.is_numeric_dtype(series):
            return 'numeric'
        else:
            return 'categorical'
    
    def _determine_significance(self, p_value: float) -> str:
        """Determine statistical significance level"""
        if p_value < 0.001:
            return 'highly_significant'
        elif p_value < self.config.p_value_threshold:
            return 'significant'
        else:
            return 'not_significant'
    
    def _determine_strength(self, abs_corr: float) -> str:
        """Determine correlation strength"""
        if abs_corr >= self.config.very_strong_correlation:
            return 'very_strong'
        elif abs_corr >= self.config.strong_correlation:
            return 'strong'
        elif abs_corr >= self.config.min_correlation:
            return 'moderate'
        else:
            return 'weak'
    
    def get_top_features(self, 
                        correlations: List[FeatureCorrelation],
                        n: Optional[int] = None) -> List[str]:
        """
        Get top N features by correlation strength
        """
        if n is None:
            n = self.config.top_features_for_graphs
        
        # Filter significant correlations
        significant = [c for c in correlations if c.significance != 'not_significant']
        
        # Sort by absolute correlation
        significant.sort(key=lambda x: abs(x.correlation_value), reverse=True)
        
        return [c.feature_name for c in significant[:n]]
    
    def generate_correlation_summary(self, 
                                    correlations: List[FeatureCorrelation]) -> Dict:
        """
        Generate a summary of correlation analysis
        """
        if not correlations:
            return {
                'n_features_analyzed': 0,
                'n_significant': 0,
                'message': 'No significant correlations found'
            }
        
        n_significant = len([c for c in correlations if c.significance != 'not_significant'])
        n_strong = len([c for c in correlations if c.relationship_strength in ['strong', 'very_strong']])
        
        top_5 = correlations[:5]
        
        return {
            'n_features_analyzed': len(correlations),
            'n_significant': n_significant,
            'n_strong': n_strong,
            'top_features': [
                {
                    'feature': c.feature_name,
                    'correlation': c.correlation_value,
                    'p_value': c.p_value,
                    'strength': c.relationship_strength,
                    'test': c.test_type
                }
                for c in top_5
            ],
            'message': f"Found {n_significant} significant correlations, {n_strong} strong relationships"
        }


# ================================
# ADVANCED ANALYSIS FUNCTIONS
# ================================

def compute_feature_importance_matrix(df: pd.DataFrame, 
                                     target_col: str) -> pd.DataFrame:
    """
    Compute pairwise feature importance/correlation matrix
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if target_col in numeric_cols:
        corr_matrix = df[numeric_cols].corr()
        return corr_matrix
    else:
        return pd.DataFrame()


def detect_multicollinearity(df: pd.DataFrame, 
                             threshold: float = 0.8) -> List[Tuple[str, str, float]]:
    """
    Detect highly correlated feature pairs (multicollinearity)
    
    Returns:
        List of (feature1, feature2, correlation) tuples
    """
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    
    high_corr_pairs = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = abs(corr_matrix.iloc[i, j])
            if corr_val >= threshold:
                high_corr_pairs.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_val
                ))
    
    return high_corr_pairs
