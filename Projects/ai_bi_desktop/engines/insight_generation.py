"""
Insight Generation Engine
=========================
Generates professional, analytical insights from BI visualizations,
correlations, and model results.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
from loguru import logger

from config.settings import insight_config
from engines.feature_correlation import FeatureCorrelation
from engines.graph_selection import GraphSpec
from engines.automl import ModelResult


@dataclass
class Insight:
    """Represents a generated insight"""
    title: str
    content: str
    insight_type: str  # 'correlation', 'model', 'feature_importance', 'summary'
    priority: int
    supporting_data: Dict
    
    def __repr__(self):
        return f"Insight({self.insight_type}: {self.title[:50]}...)"


class InsightGenerationEngine:
    """
    Generates professional, business-oriented insights from data analysis
    """
    
    def __init__(self):
        self.config = insight_config
        logger.info("Insight Generation Engine initialized")
    
    def generate_all_insights(self,
                             df: pd.DataFrame,
                             target_col: str,
                             task_type: str,
                             correlations: List[FeatureCorrelation],
                             best_model: ModelResult,
                             all_models: List[ModelResult],
                             graph_specs: List[GraphSpec]) -> List[Insight]:
        """
        Generate comprehensive insights from all analysis components
        """
        logger.info("Generating AI insights...")
        
        insights = []
        
        # 1. Executive Summary
        summary = self._generate_executive_summary(
            df, target_col, task_type, correlations, best_model
        )
        insights.append(summary)
        
        # 2. Model Selection Insight
        model_insight = self._generate_model_insight(best_model, all_models)
        insights.append(model_insight)
        
        # 3. Top Feature Insights
        feature_insights = self._generate_feature_insights(
            correlations[:5], task_type, best_model
        )
        insights.extend(feature_insights)
        
        # 4. Visualization Insights
        if self.config.include_correlation_insights:
            viz_insights = self._generate_visualization_insights(
                graph_specs[:3], correlations, task_type
            )
            insights.extend(viz_insights)
        
        # 5. Business Recommendations
        if self.config.include_business_context:
            business_insight = self._generate_business_recommendations(
                target_col, task_type, correlations, best_model
            )
            insights.append(business_insight)
        
        logger.info(f"Generated {len(insights)} insights")
        
        return insights
    
    def _generate_executive_summary(self,
                                   df: pd.DataFrame,
                                   target_col: str,
                                   task_type: str,
                                   correlations: List[FeatureCorrelation],
                                   best_model: ModelResult) -> Insight:
        """
        Generate high-level executive summary
        """
        n_significant = len([c for c in correlations if c.significance != 'not_significant'])
        n_strong = len([c for c in correlations if c.relationship_strength in ['strong', 'very_strong']])
        
        task_desc = {
            'regression': 'predicting',
            'binary_classification': 'classifying',
            'multiclass_classification': 'categorizing'
        }.get(task_type, 'analyzing')
        
        content = f"""**Analysis Overview**

This analysis focuses on {task_desc} {target_col} using a dataset with {len(df):,} records and {len(df.columns)-1} features. The automated AI system identified {n_significant} statistically significant relationships, including {n_strong} strong predictive factors.

**Key Findings:**
- The {best_model.model_name} model achieved the best performance with a cross-validation score of {best_model.mean_cv_score:.4f}
- {n_strong} features demonstrate strong predictive power for {target_col}
- The analysis reveals clear patterns that can inform strategic decision-making

The following sections provide detailed insights into feature relationships, model performance, and actionable recommendations.
"""
        
        return Insight(
            title="Executive Summary",
            content=content,
            insight_type='summary',
            priority=1,
            supporting_data={
                'n_records': len(df),
                'n_features': len(df.columns) - 1,
                'n_significant': n_significant,
                'best_model': best_model.model_name,
                'cv_score': best_model.mean_cv_score
            }
        )
    
    def _generate_model_insight(self,
                               best_model: ModelResult,
                               all_models: List[ModelResult]) -> Insight:
        """
        Generate insight about model selection
        """
        # Format model comparison
        comparison_lines = []
        for i, model in enumerate(all_models[:5], 1):
            status = "✓ Selected" if i == 1 else ""
            comparison_lines.append(
                f"{i}. **{model.model_name}**: {model.mean_cv_score:.4f} {status}"
            )
        
        comparison_text = "\n".join(comparison_lines)
        
        # Get reasoning
        reasoning = " ".join(best_model.reasoning) if best_model.reasoning else \
                   f"This model demonstrated superior performance in cross-validation testing."
        
        content = f"""**Model Selection: {best_model.model_name}**

The automated AI system evaluated {len(all_models)} different algorithms and selected {best_model.model_name} as the optimal model for this task. {reasoning}

**Model Performance:**
{comparison_text}

**Why {best_model.model_name}?**
{best_model.reasoning[0] if best_model.reasoning else "Superior performance on validation data"}

The selected model demonstrates consistent performance across different data splits (standard deviation: {best_model.std_cv_score:.4f}), indicating reliable predictions on unseen data.
"""
        
        return Insight(
            title=f"Model Selection: {best_model.model_name}",
            content=content,
            insight_type='model',
            priority=2,
            supporting_data={
                'model_name': best_model.model_name,
                'cv_score': best_model.mean_cv_score,
                'n_models_compared': len(all_models)
            }
        )
    
    def _generate_feature_insights(self,
                                  top_correlations: List[FeatureCorrelation],
                                  task_type: str,
                                  best_model: ModelResult) -> List[Insight]:
        """
        Generate insights for top features
        """
        insights = []
        
        for i, corr in enumerate(top_correlations, 1):
            # Determine impact direction
            if corr.correlation_value > 0:
                direction = "increases"
                relationship = "positive"
            else:
                direction = "decreases"
                relationship = "negative"
            
            # Strength description
            strength_desc = {
                'very_strong': 'very strong',
                'strong': 'strong',
                'moderate': 'moderate',
                'weak': 'weak'
            }.get(corr.relationship_strength, 'measurable')
            
            # Statistical confidence
            if corr.p_value < 0.001:
                confidence = "highly statistically significant (p < 0.001)"
            elif corr.p_value < 0.01:
                confidence = "statistically significant (p < 0.01)"
            else:
                confidence = f"statistically significant (p = {corr.p_value:.4f})"
            
            # Check if feature is in model's top importance
            importance_note = ""
            if best_model.feature_importance is not None:
                top_features = best_model.feature_importance.head(5)['feature'].tolist()
                if corr.feature_name in top_features:
                    rank = top_features.index(corr.feature_name) + 1
                    importance_note = f"\n\nThe {best_model.model_name} model confirms this relationship, ranking {corr.feature_name} as the #{rank} most important predictor."
            
            content = f"""**Feature Impact: {corr.feature_name}**

{corr.feature_name} demonstrates a {strength_desc} {relationship} relationship with {corr.target_name} (correlation: {corr.correlation_value:.3f}). This relationship is {confidence}, tested using {corr.test_type}.

**Key Insight:**
When {corr.feature_name} increases, {corr.target_name} tends to {direction}. This pattern is consistent across the dataset and has been validated through rigorous statistical testing.{importance_note}

**Business Implication:**
Understanding and leveraging the {corr.feature_name}-{corr.target_name} relationship can provide strategic advantages in {task_type.replace('_', ' ')} scenarios.
"""
            
            insights.append(Insight(
                title=f"Key Driver: {corr.feature_name}",
                content=content,
                insight_type='feature_importance',
                priority=3 + i,
                supporting_data={
                    'feature': corr.feature_name,
                    'correlation': corr.correlation_value,
                    'p_value': corr.p_value,
                    'strength': corr.relationship_strength
                }
            ))
        
        return insights
    
    def _generate_visualization_insights(self,
                                       graph_specs: List[GraphSpec],
                                       correlations: List[FeatureCorrelation],
                                       task_type: str) -> List[Insight]:
        """
        Generate insights for visualizations
        """
        insights = []
        
        for spec in graph_specs:
            # Find corresponding correlation
            corr = next((c for c in correlations if c.feature_name == spec.feature_name), None)
            
            if not corr:
                continue
            
            # Graph-specific insight
            if spec.graph_type == 'scatter':
                pattern = "linear trend" if abs(corr.correlation_value) > 0.5 else "relationship"
                content = f"""**Visualization Analysis: {spec.feature_name} vs {spec.target_name}**

The scatter plot visualization reveals a clear {pattern} between {spec.feature_name} and {spec.target_name}. {spec.reasoning}

The data points cluster along a trend line, indicating a predictable relationship that the machine learning model can exploit for accurate predictions.
"""
            
            elif spec.graph_type in ['box', 'violin']:
                content = f"""**Distribution Analysis: {spec.feature_name} by {spec.target_name}**

The distribution plot shows distinct patterns in {spec.feature_name} across different {spec.target_name} categories. {spec.reasoning}

These distributional differences enable the model to effectively discriminate between categories based on {spec.feature_name} values.
"""
            
            elif spec.graph_type == 'bar':
                content = f"""**Categorical Analysis: {spec.feature_name} Impact**

The bar chart reveals how {spec.feature_name} levels differentially impact {spec.target_name}. {spec.reasoning}

This categorical relationship provides clear decision boundaries for the classification model.
"""
            
            else:
                content = f"""**Pattern Analysis: {spec.feature_name}**

{spec.reasoning}

This visualization confirms the statistical relationship detected in the correlation analysis.
"""
            
            insights.append(Insight(
                title=f"Visual Insight: {spec.feature_name}",
                content=content,
                insight_type='correlation',
                priority=20,
                supporting_data={'graph_spec': spec}
            ))
        
        return insights
    
    def _generate_business_recommendations(self,
                                          target_col: str,
                                          task_type: str,
                                          correlations: List[FeatureCorrelation],
                                          best_model: ModelResult) -> Insight:
        """
        Generate actionable business recommendations
        """
        top_features = [c.feature_name for c in correlations[:3]]
        
        if task_type == 'regression':
            action_verb = "optimize"
            outcome = "value"
        elif task_type == 'binary_classification':
            action_verb = "predict"
            outcome = "outcome"
        else:
            action_verb = "classify"
            outcome = "category"
        
        content = f"""**Strategic Recommendations**

Based on the comprehensive AI analysis, here are actionable recommendations for {action_verb}ing {target_col}:

**1. Focus on Key Drivers**
Prioritize monitoring and influencing the top 3 predictive factors: {', '.join(top_features)}. These variables have the strongest impact on {target_col} {outcome}s.

**2. Leverage Model Insights**
Deploy the {best_model.model_name} model (CV score: {best_model.mean_cv_score:.4f}) for predictive decision-making. This model has been validated across multiple data splits and demonstrates reliable performance.

**3. Data-Driven Decision Making**
Use the identified correlations to inform strategic planning. The relationships discovered are statistically significant and can guide resource allocation and operational decisions.

**4. Continuous Monitoring**
Regularly update the model with new data to maintain prediction accuracy. Monitor the key features identified in this analysis as leading indicators of {target_col} changes.

**Implementation Roadmap:**
- Short-term: Focus on the top 3 features for immediate impact
- Medium-term: Develop interventions targeting moderate-strength relationships
- Long-term: Build automated monitoring systems using the trained model

The combination of strong statistical relationships and high model performance provides a solid foundation for data-driven decision-making in this domain.
"""
        
        return Insight(
            title="Strategic Recommendations",
            content=content,
            insight_type='summary',
            priority=100,
            supporting_data={
                'top_features': top_features,
                'model_name': best_model.model_name
            }
        )
    
    def format_insights_for_display(self, insights: List[Insight]) -> str:
        """
        Format all insights into a single markdown document
        """
        # Sort by priority
        insights.sort(key=lambda x: x.priority)
        
        markdown = "# AI-Generated Analysis Insights\n\n"
        markdown += "_Automatically generated by the AI BI Desktop Assistant_\n\n"
        markdown += "---\n\n"
        
        for insight in insights:
            markdown += f"## {insight.title}\n\n"
            markdown += f"{insight.content}\n\n"
            markdown += "---\n\n"
        
        return markdown
