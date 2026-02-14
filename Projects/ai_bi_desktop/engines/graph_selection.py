"""
Auto Graph Selection Engine
===========================
Intelligently selects the optimal visualization type for each feature-target relationship
based on data types, distributions, correlation strength, and model type.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from loguru import logger

from config.settings import graph_selection_config
from engines.feature_correlation import FeatureCorrelation


@dataclass
class GraphSpec:
    """Specification for a generated graph"""
    graph_type: str
    feature_name: str
    target_name: str
    title: str
    config: Dict[str, Any]
    priority: int
    reasoning: str
    
    def __repr__(self):
        return f"GraphSpec({self.graph_type}: {self.feature_name} vs {self.target_name})"


class AutoGraphSelectionEngine:
    """
    Intelligent graph selection system that automatically chooses
    the best visualization based on data characteristics
    """
    
    def __init__(self):
        self.config = graph_selection_config
        logger.info("Auto Graph Selection Engine initialized")
    
    def select_graphs(self,
                     df: pd.DataFrame,
                     target_col: str,
                     task_type: str,
                     correlations: List[FeatureCorrelation],
                     top_n_features: Optional[int] = None) -> List[GraphSpec]:
        """
        Main method to select optimal graphs for features
        
        Args:
            df: Input dataframe
            target_col: Target column name
            task_type: ML task type
            correlations: List of feature correlations
            top_n_features: Number of top features to visualize
            
        Returns:
            List of GraphSpec objects
        """
        if top_n_features is None:
            top_n_features = min(len(correlations), self.config.max_graphs_per_page)
        
        logger.info(f"Selecting graphs for top {top_n_features} features")
        
        # Get top features
        top_correlations = correlations[:top_n_features]
        
        graph_specs = []
        
        for corr in top_correlations:
            try:
                spec = self._select_graph_for_feature(
                    df, corr.feature_name, target_col, task_type, corr
                )
                if spec:
                    graph_specs.append(spec)
            except Exception as e:
                logger.warning(f"Failed to create graph spec for {corr.feature_name}: {e}")
        
        # Sort by priority
        graph_specs.sort(key=lambda x: x.priority)
        
        logger.info(f"Generated {len(graph_specs)} graph specifications")
        
        return graph_specs
    
    def _select_graph_for_feature(self,
                                  df: pd.DataFrame,
                                  feature: str,
                                  target: str,
                                  task_type: str,
                                  corr: FeatureCorrelation) -> Optional[GraphSpec]:
        """
        Select the best graph type for a specific feature-target pair
        
        Decision tree:
        1. Both numeric → Scatter plot with trend line
        2. Numeric feature, categorical target → Box plot or Violin plot
        3. Categorical feature, numeric target → Bar chart or Box plot
        4. Both categorical → Grouped bar chart or Heatmap
        """
        
        feature_type = self._get_column_type(df[feature])
        target_type = self._get_column_type(df[target])
        
        # CASE 1: Both numeric
        if feature_type == 'numeric' and target_type == 'numeric':
            return self._create_scatter_spec(df, feature, target, corr)
        
        # CASE 2: Numeric feature, categorical target
        elif feature_type == 'numeric' and target_type == 'categorical':
            # Choose between box plot and violin plot based on data size
            if len(df) > 1000:
                return self._create_box_plot_spec(df, feature, target, corr)
            else:
                return self._create_violin_plot_spec(df, feature, target, corr)
        
        # CASE 3: Categorical feature, numeric target
        elif feature_type == 'categorical' and target_type == 'numeric':
            return self._create_bar_chart_spec(df, feature, target, corr)
        
        # CASE 4: Both categorical
        elif feature_type == 'categorical' and target_type == 'categorical':
            # Choose between grouped bar and heatmap based on cardinality
            if df[feature].nunique() <= 10 and df[target].nunique() <= 10:
                return self._create_grouped_bar_spec(df, feature, target, corr)
            else:
                return self._create_heatmap_spec(df, feature, target, corr)
        
        return None
    
    def _create_scatter_spec(self,
                            df: pd.DataFrame,
                            feature: str,
                            target: str,
                            corr: FeatureCorrelation) -> GraphSpec:
        """Create specification for scatter plot with trend line"""
        
        # Sample if too many points
        if len(df) > self.config.max_points_in_scatter:
            sample_df = df.sample(n=self.config.max_points_in_scatter, random_state=42)
        else:
            sample_df = df
        
        direction = "positive" if corr.correlation_value > 0 else "negative"
        
        config = {
            'x': feature,
            'y': target,
            'data_frame': sample_df,
            'trendline': 'ols',  # Ordinary Least Squares trend line
            'title': f'{feature} vs {target}',
            'labels': {feature: feature, target: target},
            'opacity': 0.6,
            'color_discrete_sequence': ['#636EFA']
        }

        reasoning = f"Scatter plot with trend line shows {direction} {corr.relationship_strength} " \
                   f"relationship (r={corr.correlation_value:.3f}, {corr.test_type})"
        
        return GraphSpec(
            graph_type='scatter',
            feature_name=feature,
            target_name=target,
            title=f'{feature} vs {target}',
            config=config,
            priority=1,
            reasoning=reasoning
        )
    
    def _create_box_plot_spec(self,
                             df: pd.DataFrame,
                             feature: str,
                             target: str,
                             corr: FeatureCorrelation) -> GraphSpec:
        """Create specification for box plot"""
        
        config = {
            'x': target,
            'y': feature,
            'data_frame': df,
            'title': f'Distribution of {feature} by {target}',
            'labels': {target: target, feature: feature},
            'color': target,
            'notched': True  # Show confidence interval
        }
        
        reasoning = f"Box plot reveals distribution differences across {target} categories " \
                   f"({corr.relationship_strength} relationship, {corr.test_type})"
        
        return GraphSpec(
            graph_type='box',
            feature_name=feature,
            target_name=target,
            title=f'Distribution of {feature} by {target}',
            config=config,
            priority=2,
            reasoning=reasoning
        )
    
    def _create_violin_plot_spec(self,
                                df: pd.DataFrame,
                                feature: str,
                                target: str,
                                corr: FeatureCorrelation) -> GraphSpec:
        """Create specification for violin plot"""
        
        config = {
            'x': target,
            'y': feature,
            'data_frame': df,
            'title': f'Distribution of {feature} by {target}',
            'labels': {target: target, feature: feature},
            'color': target,
            'box': True,  # Show box plot inside
            'points': 'outliers'  # Show outlier points
        }
        
        reasoning = f"Violin plot shows detailed distribution shape across {target} categories " \
                   f"({corr.relationship_strength} relationship)"
        
        return GraphSpec(
            graph_type='violin',
            feature_name=feature,
            target_name=target,
            title=f'Distribution of {feature} by {target}',
            config=config,
            priority=3,
            reasoning=reasoning
        )
    
    def _create_bar_chart_spec(self,
                              df: pd.DataFrame,
                              feature: str,
                              target: str,
                              corr: FeatureCorrelation) -> GraphSpec:
        """Create specification for bar chart"""
        
        # Limit categories if too many
        n_categories = df[feature].nunique()
        if n_categories > self.config.max_categories_in_bar:
            # Keep top categories by frequency
            top_categories = df[feature].value_counts().head(
                self.config.max_categories_in_bar
            ).index
            plot_df = df[df[feature].isin(top_categories)]
        else:
            plot_df = df
        
        # Aggregate data
        agg_df = plot_df.groupby(feature)[target].mean().reset_index()
        agg_df = agg_df.sort_values(target, ascending=False)
        
        config = {
            'x': feature,
            'y': target,
            'data_frame': agg_df,
            'title': f'Average {target} by {feature}',
            'labels': {feature: feature, target: f'Average {target}'},
            'color': target,
            'text': target,
            'color_continuous_scale': 'Blues'
        }
        
        reasoning = f"Bar chart shows average {target} across {feature} categories " \
                   f"({corr.relationship_strength} relationship, {corr.test_type})"
        
        return GraphSpec(
            graph_type='bar',
            feature_name=feature,
            target_name=target,
            title=f'Average {target} by {feature}',
            config=config,
            priority=4,
            reasoning=reasoning
        )
    
    def _create_grouped_bar_spec(self,
                                df: pd.DataFrame,
                                feature: str,
                                target: str,
                                corr: FeatureCorrelation) -> GraphSpec:
        """Create specification for grouped bar chart (both categorical)"""
        
        # Create contingency table
        contingency = pd.crosstab(df[feature], df[target], normalize='index') * 100
        contingency = contingency.reset_index()
        
        # Melt for plotly
        melted = contingency.melt(id_vars=feature, var_name=target, value_name='Percentage')
        
        config = {
            'x': feature,
            'y': 'Percentage',
            'color': target,
            'data_frame': melted,
            'title': f'Distribution of {target} by {feature}',
            'labels': {feature: feature, target: target, 'Percentage': '% of Total'},
            'barmode': 'group'
        }
        
        reasoning = f"Grouped bar chart shows {target} distribution across {feature} categories " \
                   f"({corr.relationship_strength} association, {corr.test_type})"
        
        return GraphSpec(
            graph_type='grouped_bar',
            feature_name=feature,
            target_name=target,
            title=f'Distribution of {target} by {feature}',
            config=config,
            priority=5,
            reasoning=reasoning
        )
    
    def _create_heatmap_spec(self,
                            df: pd.DataFrame,
                            feature: str,
                            target: str,
                            corr: FeatureCorrelation) -> GraphSpec:
        """Create specification for heatmap (both categorical)"""
        
        # Create contingency table
        contingency = pd.crosstab(df[feature], df[target])
        
        config = {
            'z': contingency.values,
            'x': contingency.columns.tolist(),
            'y': contingency.index.tolist(),
            'title': f'Relationship between {feature} and {target}',
            'colorscale': 'Blues',
            'labels': {'x': target, 'y': feature, 'color': 'Count'}
        }
        
        reasoning = f"Heatmap visualizes frequency patterns between {feature} and {target} " \
                   f"({corr.relationship_strength} association, {corr.test_type})"
        
        return GraphSpec(
            graph_type='heatmap',
            feature_name=feature,
            target_name=target,
            title=f'Relationship between {feature} and {target}',
            config=config,
            priority=5,
            reasoning=reasoning
        )
    
    def create_plotly_figure(self, spec: GraphSpec) -> go.Figure:
        """
        Create actual Plotly figure from GraphSpec
        """
        try:
            if spec.graph_type == 'scatter':
                fig = px.scatter(**spec.config)
                
            elif spec.graph_type == 'box':
                fig = px.box(**spec.config)
                
            elif spec.graph_type == 'violin':
                fig = px.violin(**spec.config)
                
            elif spec.graph_type == 'bar':
                fig = px.bar(**spec.config)
                
            elif spec.graph_type == 'grouped_bar':
                fig = px.bar(**spec.config)
                
            elif spec.graph_type == 'heatmap':
                fig = go.Figure(data=go.Heatmap(
                    z=spec.config['z'],
                    x=spec.config['x'],
                    y=spec.config['y'],
                    colorscale=spec.config['colorscale']
                ))
                fig.update_layout(title=spec.config['title'])
            
            else:
                raise ValueError(f"Unknown graph type: {spec.graph_type}")
            
            # Apply theme and styling
            fig.update_layout(
                template=self.config.plotly_theme,
                showlegend=True,
                hovermode='closest',
                height=500
            )
            
            if self.config.show_grid:
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create Plotly figure for {spec.graph_type}: {e}")
            # Return empty figure
            return go.Figure()
    
    def _get_column_type(self, series: pd.Series) -> str:
        """Determine if column is numeric or categorical"""
        if pd.api.types.is_numeric_dtype(series):
            return 'numeric'
        else:
            return 'categorical'
    
    def create_feature_importance_plot(self,
                                      correlations: List[FeatureCorrelation],
                                      top_n: int = 15) -> go.Figure:
        """
        Create a horizontal bar chart of feature importance/correlation
        """
        top_corrs = correlations[:top_n]
        
        features = [c.feature_name for c in top_corrs]
        values = [abs(c.correlation_value) for c in top_corrs]
        colors = ['#FF6B6B' if c.correlation_value < 0 else '#4ECDC4' 
                 for c in top_corrs]
        
        fig = go.Figure(go.Bar(
            x=values,
            y=features,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{v:.3f}" for v in values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f'Top {top_n} Feature Correlations',
            xaxis_title='Absolute Correlation',
            yaxis_title='Feature',
            template=self.config.plotly_theme,
            height=max(400, top_n * 30),
            showlegend=False
        )
        
        fig.update_yaxes(autorange="reversed")  # Highest at top
        
        return fig
    
    def create_correlation_matrix(self, df: pd.DataFrame) -> go.Figure:
        """
        Create correlation matrix heatmap for numeric features
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return go.Figure()
        
        corr_matrix = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Feature Correlation Matrix',
            template=self.config.plotly_theme,
            height=max(500, len(corr_matrix) * 40),
            width=max(500, len(corr_matrix) * 40)
        )
        
        return fig
