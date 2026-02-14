# 🤖 AI BI Desktop Application
[להסבר בעברית לחץ פה](https://github.com/saharYaccov/portfolio/blob/main/Projects/ai_bi_desktop/ReadmeHe.md)

## Revolutionary AI-Powered Business Intelligence & AutoML Platform

A next-generation desktop application that combines **automated Business Intelligence**, **AutoML**, and **AI-generated insights** into a single intelligent system that thinks for you.

---

## 🌟 Key Features

### 🎯 **Automatic Target Detection**
- Intelligently identifies the most likely target column(s)
- Uses semantic analysis, statistical properties, and ML heuristics
- Provides confidence scores and reasoning for each candidate

### 📊 **Intelligent BI Dashboard**
- Automatically generates publication-quality visualizations
- Selects optimal graph types based on data characteristics
- Interactive Plotly visualizations (Tableau/Power BI quality)
- Statistical significance testing for all relationships

### 🤖 **Production-Grade AutoML**
- Uses Optuna for hyperparameter optimization
- Evaluates multiple model types (Random Forest, XGBoost, LightGBM, CatBoost, etc.)
- Cross-validation with stratified sampling
- Complete preprocessing pipelines

### 🔍 **Full Model Transparency**
- Always shows which model was selected and why
- Model comparison tables with performance metrics
- Feature importance rankings
- Hyperparameter details

### 💡 **AI-Generated Insights**
- Professional, business-oriented written insights
- Combines correlation analysis, model findings, and statistical tests
- Executive summaries and strategic recommendations
- Export insights as Markdown reports

### 🖥️ **Background Desktop Service**
- Runs silently in system tray
- Monitors Downloads folder for new datasets
- Low resource consumption (<100MB RAM)
- Quick-access dashboard launcher

### 🧠 **Adaptive Learning** (Future)
- Learns from user preferences over time
- Improves model selection based on historical performance
- Adapts graph selection to user interactions

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download the repository
cd ai_bi_desktop

# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run the application
python main.py
```

### Basic Usage

**1. Background Service (System Tray)**
```bash
python main.py
# Right-click tray icon → "Open Dashboard"
```

**2. Dashboard Only**
```bash
python main.py --dashboard
# Opens at http://localhost:7860
```

**3. Direct Analysis**
```bash
python main.py --analyze data.csv
python main.py --analyze data.csv --target price
```

---

## 📁 Project Structure

```
ai_bi_desktop/
├── main.py                    # Main entry point
├── requirements.txt           # Dependencies
│
├── config/
│   └── settings.py           # All configuration parameters
│
├── engines/                   # Intelligent AI engines
│   ├── target_detection.py   # Automatic target detection
│   ├── feature_correlation.py # Statistical correlation analysis
│   ├── graph_selection.py    # Auto graph selection
│   ├── automl.py             # Optuna-based AutoML
│   └── insight_generation.py # AI insight generator
│
├── core/
│   ├── orchestrator.py       # Main AI orchestrator
│   └── background_service.py # Desktop service
│
├── ui/
│   └── gradio_app.py         # Multi-page Gradio dashboard
│
├── data/                     # User data directory
├── models/                   # Saved models
├── cache/                    # Analysis cache
└── logs/                     # Application logs
```

---

## 🎨 Dashboard Features

### 📊 **BI Dashboard Tab**
- **Dataset Overview**: Statistics, data types, missing values
- **Target Information**: Detection reasoning and confidence
- **Feature Importance**: Ranked by correlation strength
- **Top Visualizations**: 6 automatically selected graphs
- **Correlation Matrix**: Feature relationships heatmap

### 🤖 **Machine Learning Tab**
- **Best Model Display**: Selected model with reasoning
- **Performance Metrics**: CV scores, accuracy, R², etc.
- **Model Comparison**: All models ranked by performance
- **Feature Importance**: Model-based importance rankings
- **Hyperparameters**: Optimized parameter values

### 💡 **AI Insights Tab**
- **Executive Summary**: High-level analysis overview
- **Model Selection Insight**: Why this model was chosen
- **Feature Insights**: Deep dive into top predictive features
- **Visualization Insights**: What each graph reveals
- **Strategic Recommendations**: Actionable business advice
- **Download Report**: Export as Markdown

---

## 🔧 Configuration

Edit `config/settings.py` to customize:

### Application Settings
```python
# Gradio dashboard
gradio_port = 7860
gradio_share = False

# Resource limits
max_memory_mb = 2048
max_cpu_percent = 50.0
```

### Data Processing
```python
# File limits
max_file_size_mb = 500.0
max_rows = 1_000_000
max_columns = 1000

# Missing data
missing_threshold = 0.5  # Drop columns with >50% missing
```

### Target Detection
```python
# Keywords for semantic matching
target_keywords = ['target', 'label', 'y', 'outcome', 'price', 'sales', ...]

# Confidence thresholds
min_confidence_score = 0.3
max_target_candidates = 3
```

### AutoML Settings
```python
# Optuna optimization
n_trials = 50
optimization_timeout_seconds = 300

# Cross-validation
cv_folds = 5
stratified_cv = True
```

---

## 📊 Example Workflow

### Step 1: Upload Dataset
- Drag & drop CSV/Excel file
- Or use file picker
- Optionally specify target column

### Step 2: Automated Analysis
The system automatically:
1. ✅ Detects target column(s)
2. ✅ Analyzes feature correlations
3. ✅ Selects optimal visualizations
4. ✅ Trains and optimizes ML models
5. ✅ Generates professional insights

### Step 3: Explore Results

**BI Dashboard:**
- View interactive visualizations
- Understand feature relationships
- Identify patterns and outliers

**ML Dashboard:**
- Review model performance
- Compare different algorithms
- Understand feature importance

**AI Insights:**
- Read professional analysis
- Get strategic recommendations
- Download full report

---

## 🧪 Supported Use Cases

### Regression Tasks
- Price prediction
- Sales forecasting
- Risk scoring
- Demand prediction

### Binary Classification
- Churn prediction
- Fraud detection
- Credit default
- Medical diagnosis

### Multiclass Classification
- Customer segmentation
- Product categorization
- Sentiment analysis
- Priority classification

---

## 🔬 Technical Details

### Models Supported
- **Tree-Based**: Random Forest, XGBoost, LightGBM, CatBoost, Gradient Boosting
- **Linear**: Logistic Regression, Linear Regression, Ridge, Lasso
- **Future**: Neural Networks, SVMs, Ensemble methods

### Statistical Tests
- **Numeric-Numeric**: Pearson, Spearman correlation
- **Numeric-Categorical**: Point-Biserial, ANOVA
- **Categorical-Categorical**: Chi-Square (Cramér's V)
- **Universal**: Mutual Information

### Visualizations
- Scatter plots with trend lines
- Box plots and violin plots
- Bar charts and grouped bars
- Heatmaps and correlation matrices
- Feature importance plots
- Model comparison charts

---

## 🎯 Design Philosophy

### 1. **Zero Configuration**
No manual setup required. The system makes intelligent decisions automatically.

### 2. **Full Transparency**
Every decision is explained. You always know what the system is doing and why.

### 3. **Production Quality**
Not a toy. Built with real-world enterprise BI and ML requirements in mind.

### 4. **Explainability First**
Model selection, feature importance, and insights are always clearly communicated.

### 5. **Professional Outputs**
Publication-quality visualizations and business-oriented insights.

---

## 🚦 System Requirements

- **Python**: 3.10+
- **RAM**: 2GB minimum, 4GB recommended
- **OS**: Windows, macOS, Linux
- **Optional**: GPU for deep learning models (future)

---

## 📝 Command Line Reference

```bash
# Start background service (default)
python main.py

# Launch dashboard directly
python main.py --dashboard

# Analyze a file
python main.py --analyze data.csv

# Analyze with specific target
python main.py --analyze data.csv --target sales

# Use custom port
python main.py --dashboard --port 8080

# Create public share link
python main.py --dashboard --share

# Show version
python main.py --version
```

---

## 🛠️ Advanced Features

### Caching
Analysis results are cached automatically. Re-uploading the same file retrieves cached results instantly.

### Logging
All operations are logged to `logs/` directory with rotation and retention policies.

### Resource Monitoring
Background service monitors CPU and memory usage, with configurable limits.

### File Monitoring
Automatically detects new CSV/Excel files in Downloads folder and offers to analyze them.

---

## 🎓 Example Datasets

Try the system with popular datasets:

1. **Regression**: Boston Housing, California Housing
2. **Binary Classification**: Titanic, Credit Card Fraud
3. **Multiclass**: Iris, Wine Quality, Customer Segments

Download from: https://www.kaggle.com/datasets

---

## 🐛 Troubleshooting

**Dashboard won't open:**
- Check if port 7860 is available
- Try different port: `python main.py --dashboard --port 8080`

**Out of memory:**
- Reduce `max_rows` in `config/settings.py`
- Enable sampling for large datasets

**Model training too slow:**
- Reduce `n_trials` in AutoML settings
- Set `optimization_timeout_seconds` lower

**System tray icon not showing:**
- Install pystray: `pip install pystray`
- Run dashboard directly: `python main.py --dashboard`

---

## 🔮 Roadmap

### Version 1.1
- [ ] Deep learning models (PyTorch/TensorFlow)
- [ ] Time series forecasting
- [ ] Advanced feature engineering
- [ ] Model deployment APIs

### Version 1.2
- [ ] Real-time data streaming
- [ ] Collaborative features
- [ ] Cloud integration
- [ ] Mobile companion app

### Version 2.0
- [ ] Natural language queries
- [ ] Automated report generation
- [ ] A/B testing capabilities
- [ ] Multi-model ensembling

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 👏 Acknowledgments

Built with:
- **Gradio** - Interactive ML interfaces
- **Plotly** - Beautiful visualizations
- **Optuna** - Hyperparameter optimization
- **Scikit-learn** - ML foundations
- **XGBoost, LightGBM, CatBoost** - Gradient boosting excellence
- **SHAP** - Model explainability

---

## 📧 Support

For issues, questions, or feature requests, please check the documentation or create an issue.

---

**🚀 Start analyzing smarter today with AI BI Desktop!**
