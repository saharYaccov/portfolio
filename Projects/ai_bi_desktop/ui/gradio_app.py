"""
Gradio Dashboard
===============
Multi-page interactive dashboard for the AI BI Desktop Application
"""

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from typing import Optional, Tuple
from pathlib import Path
from loguru import logger
import joblib

from core.orchestrator import AIOrchestrator, AnalysisResult
from engines.graph_selection import AutoGraphSelectionEngine
from config.settings import app_config
from sklearn.metrics import accuracy_score, r2_score


class GradioDashboard:
    """
    Main Gradio dashboard application
    """
    
    def __init__(self):
        self.orchestrator = AIOrchestrator()
        self.graph_engine = AutoGraphSelectionEngine()
        self.current_result: Optional[AnalysisResult] = None
        self.current_file_path: Optional[str] = None  # Store file path for correlation matrix

        logger.info("Gradio Dashboard initialized")

    def create_dashboard(self) -> gr.Blocks:
        """
        Create the main multi-page Gradio dashboard
        """
        with gr.Blocks(
            title=app_config.app_name,
            theme=gr.themes.Soft(),
            css=self._get_custom_css()
        ) as dashboard:

            # Header
            gr.Markdown(f"""
            # 🤖 {app_config.app_name}
            ### Intelligent BI Analytics & AutoML Platform
            _Version {app_config.version} - Powered by AI_
            """)

            # File upload section
            with gr.Row():
                with gr.Column(scale=3):
                    file_input = gr.File(
                        label="📁 Upload Dataset (CSV or Excel)",
                        file_types=['.csv', '.xlsx', '.xls'],
                        type="filepath"
                    )

                with gr.Column(scale=1):
                    target_input = gr.Textbox(
                        label="🎯 Target Column (optional)",
                        placeholder="Leave empty for auto-detection",
                        lines=1
                    )

            analyze_btn = gr.Button(
                "🚀 Run AI Analysis",
                variant="primary",
                size="lg"
            )

            # Status/Progress
            status_output = gr.Markdown(value="Upload a dataset to begin...")

            # Tabs for different views
            with gr.Tabs() as tabs:

                # ================================
                # TAB 1: BI DASHBOARD
                # ================================
                with gr.Tab("📊 BI Dashboard"):
                    gr.Markdown("## Automated Business Intelligence Visualizations")

                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### 📈 Dataset Overview")
                            dataset_stats = gr.JSON(label="Dataset Statistics")
                            target_info = gr.Markdown("_No analysis yet_")

                        with gr.Column(scale=2):
                            gr.Markdown("### 🔥 Feature Importance")
                            importance_plot = gr.Plot()

                    gr.Markdown("### 📊 Top Feature Visualizations")
                    gr.Markdown("_Automatically selected visualizations based on statistical significance_")

                    # Container for multiple graphs
                    with gr.Row():
                        bi_plot_1 = gr.Plot()
                        bi_plot_2 = gr.Plot()

                    with gr.Row():
                        bi_plot_3 = gr.Plot()
                        bi_plot_4 = gr.Plot()

                    with gr.Row():
                        bi_plot_5 = gr.Plot()
                        bi_plot_6 = gr.Plot()

                    gr.Markdown("### 🔗 Correlation Matrix")
                    correlation_matrix = gr.Plot()

                # ================================
                # TAB 2: ML DASHBOARD
                # ================================
                with gr.Tab("🤖 Machine Learning"):
                    gr.Markdown("## AutoML Model Training & Evaluation")

                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 🏆 Best Model")
                            best_model_info = gr.Markdown("_No model trained yet_")

                            gr.Markdown("### 📊 Model Performance Metrics")
                            model_metrics = gr.JSON(label="Evaluation Metrics")

                        with gr.Column():
                            gr.Markdown("### 📈 Model Comparison")
                            model_comparison = gr.DataFrame(
                                label="All Models Performance",
                                headers=["Model", "CV Score", "Std Dev", "Status"]
                            )

                            gr.Markdown("### 🔍 Why This Model?")
                            model_reasoning = gr.Markdown("_Analysis in progress..._")

                    gr.Markdown("### 🎯 Feature Importance (Model-Based)")
                    model_feature_plot = gr.Plot()

                    '''
                    # 🔹 כאן נציג את העץ
                    gr.Markdown("### 🌳 Decision Tree")
                    tree_plot = gr.Image(label="Decision Tree")  # <-- רכיב Gradio
                    '''

                    gr.Markdown("### ⚙️ Hyperparameters")
                    hyperparameters = gr.JSON(label="Optimized Hyperparameters")

                # ================================
                # TAB 3: AI INSIGHTS
                # ================================
                with gr.Tab("💡 AI Insights"):
                    gr.Markdown("## AI-Generated Business Insights")
                    gr.Markdown("_Professional analytical insights written by AI_")

                    insights_output = gr.Markdown(
                        value="Run analysis to generate insights...",
                        line_breaks=True
                    )

                    gr.Markdown("### 📥 Download Insights Report")
                    download_btn = gr.DownloadButton(
                        label="Download Full Report (Markdown)",
                        visible=False
                    )


            # ================================
            # EVENT HANDLERS
            # ================================

            analyze_btn.click(
                fn=self.run_analysis,
                inputs=[file_input, target_input],
                outputs=[
                    status_output,
                    # BI Dashboard outputs
                    dataset_stats,
                    target_info,
                    importance_plot,
                    bi_plot_1, bi_plot_2, bi_plot_3,
                    bi_plot_4, bi_plot_5, bi_plot_6,
                    correlation_matrix,
                    # ML Dashboard outputs
                    best_model_info,
                    model_metrics,
                    model_comparison,
                    model_reasoning,
                    model_feature_plot,
                    hyperparameters,
                    # Insights outputs
                    insights_output,
                    download_btn,

                ]
            )

        return dashboard

    def run_analysis(self,
                    file_path: Optional[str],
                    target_col: Optional[str]) -> Tuple:
        """
        Main analysis workflow triggered by button click
        """
        try:
            if not file_path:
                return self._empty_outputs("❌ Please upload a dataset first")

            # Clean target column input
            target_col = target_col.strip() if target_col else None
            if target_col == "":
                target_col = None

            # Run analysis
            logger.info(f"Running analysis on {file_path}")
            result = self.orchestrator.analyze_dataset(file_path, target_col)
            self.current_result = result
            self.current_file_path = file_path  # Store for correlation matrix

            # Generate all outputs
            return self._generate_all_outputs(result, file_path)

        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            return self._empty_outputs(f"❌ Analysis failed: {str(e)}")

    def _generate_all_outputs(self, result: AnalysisResult, file_path: str) -> Tuple:
        """
        Generate all dashboard outputs from analysis result
        """
        # Status message
        status = f"""
        ✅ **Analysis Complete!**
        
        - **Target**: {result.selected_target.column_name} ({result.selected_target.task_type})
        - **Best Model**: {result.best_model.model_name}
        - **CV Score**: {result.best_model.mean_cv_score:.4f}
        - **Features Analyzed**: {len(result.correlations)}
        """

        # BI Dashboard outputs
        dataset_stats = result.dataset_info

        target_info = f"""
        ### 🎯 Selected Target: **{result.selected_target.column_name}**
        - **Task Type**: {result.selected_target.task_type.replace('_', ' ').title()}
        - **Confidence**: {result.selected_target.confidence_score:.2%}
        - **Unique Values**: {result.selected_target.n_unique}
        
        **Detection Reasoning:**
        {chr(10).join(f"- {r}" for r in result.selected_target.reasoning)}
        """

        # Feature importance plot
        importance_plot = self.graph_engine.create_feature_importance_plot(result.correlations)

        # Individual BI plots
        bi_plots = []
        for i in range(6):
            if i < len(result.graph_specs):
                spec = result.graph_specs[i]
                fig = self.graph_engine.create_plotly_figure(spec)
                bi_plots.append(fig)
            else:
                bi_plots.append(go.Figure())  # Empty plot

        # Correlation matrix
        try:
            # Load the dataframe to create correlation matrix
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:  # Excel
                df = pd.read_excel(file_path)

            correlation_matrix = self.graph_engine.create_correlation_matrix(df)
        except Exception as e:
            logger.warning(f"Failed to create correlation matrix: {e}")
            correlation_matrix = go.Figure()  # Empty figure on error
        
        # ML Dashboard outputs
        best_model_info = f"""
        ## 🏆 {result.best_model.model_name}
        
        **Performance:**
        - Cross-Validation Score: **{result.best_model.mean_cv_score:.4f}** ± {result.best_model.std_cv_score:.4f}
        - Trained on {result.dataset_info['n_rows']:,} samples
        - Using {result.dataset_info['n_columns']-1} features
        """
        
        model_metrics = result.best_model.metrics
        
        # Model comparison table
        comparison_data = []
        for i, model in enumerate(result.all_models):


            comparison_data.append([
                model.model_name,
                f"{model.mean_cv_score:.4f}",
                f"{model.std_cv_score:.4f}",
                "✅ Selected" if i == 0 else ""
            ])
        
        model_comparison = pd.DataFrame(
            comparison_data,
            columns=["Model", "CV Score", "Std Dev", "Status"]
        )
        
        model_reasoning = "**Selection Reasoning:**\n\n" + "\n".join(
            f"{i+1}. {r}" for i, r in enumerate(result.best_model.reasoning)
        )
        
        # Model feature importance plot
        if result.feature_importance_df is not None:
            top_fi = result.feature_importance_df.head(15)
            model_feature_plot = go.Figure(go.Bar(
                x=top_fi['importance'],
                y=top_fi['feature'],
                orientation='h',
                marker=dict(color='#4ECDC4')
            ))
            model_feature_plot.update_layout(
                title='Top 15 Features by Model Importance',
                xaxis_title='Importance',
                yaxis_title='Feature',
                height=500
            )
        else:
            model_feature_plot = go.Figure()
        
        hyperparameters = result.best_model.best_params
        
        # AI Insights
        insights_md = self.orchestrator.insight_engine.format_insights_for_display(result.insights)
        
        # Download button
        download_btn = gr.DownloadButton(
            label="📥 Download Full Report",
            value=self._create_report_file(result),
            visible=True
        )
        #tree_img = display_tree_in_gradio(result.best_model)
        return (
            status,
            dataset_stats, target_info, importance_plot,
            *bi_plots,
            correlation_matrix,
            best_model_info, model_metrics, model_comparison,
            model_reasoning, model_feature_plot, hyperparameters,
            insights_md,
            download_btn,
            #tree_img
        )
    
    def _empty_outputs(self, message: str) -> Tuple:
        """
        Return empty outputs with error message
        """
        empty_plot = go.Figure()
        empty_df = pd.DataFrame()
        
        return (
            message,  # status
            {}, "", empty_plot,  # BI dashboard
            empty_plot, empty_plot, empty_plot,
            empty_plot, empty_plot, empty_plot,
            empty_plot,
            "", {}, empty_df,  # ML dashboard
            "", empty_plot, {},
            "Run analysis to see insights...",  # Insights
            gr.DownloadButton(visible=False)
        )




    def _create_report_file(self, result: AnalysisResult) -> str:
        """
        Create downloadable report file
        """
        report_path = Path("/tmp/ai_bi_report.md")
        
        insights_md = self.orchestrator.insight_engine.format_insights_for_display(result.insights)
        
        with open(report_path, 'w') as f:
            f.write(insights_md)

        return str(report_path)

    def _get_custom_css(self) -> str:
        """
        Custom CSS for dashboard styling
        """
        return """
        .gradio-container {
            font-family: 'Inter', sans-serif;
        }
        
        h1 {
            color: #2C3E50;
            font-weight: 700;
        }
        
        h3 {
            color: #34495E;
            margin-top: 1.5rem;
        }
        
        .tabs {
            margin-top: 2rem;
        }
        """

def display_tree_in_gradio(model_result):
    try:
        img = plot_tree_from_model_for_gradio(model_result)
        return img
    except Exception as e:
        return None
def launch_dashboard(share: bool = False, port: int = 7860):
    """
    Launch the Gradio dashboard
    
    Args:
        share: Whether to create public link
        port: Port number for local server
    """
    dashboard_app = GradioDashboard()
    app = dashboard_app.create_dashboard()
    
    logger.info(f"Launching dashboard on port {port}")
    
    app.launch(
        share=share,
        server_port=port,
        server_name="0.0.0.0",
        show_error=True,
        quiet=False,
        allowed_paths=["/tmp"]  # <-- מוסיף הרשאה לקבצי temp

    )


if __name__ == "__main__":
    launch_dashboard()
