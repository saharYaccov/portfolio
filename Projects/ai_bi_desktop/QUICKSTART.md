# 🚀 Quick Start Guide

## Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd ai_bi_desktop
pip install -r requirements.txt --break-system-packages
```

**Note:** If you encounter installation issues:
- Use Python 3.10 or higher
- On Linux/Mac, you may need: `sudo apt-get install python3-tk`
- For system tray support: `pip install pystray pillow`

---

### Step 2: Run Examples

#### Option A: Interactive Examples Menu
```bash
python examples.py
```

Choose from:
1. **Regression Example** - Loan amount prediction
2. **Classification Example** - Customer churn prediction
3. **Launch Dashboard** - Interactive UI
4. **Run All** - Both examples

#### Option B: Direct Dashboard Launch
```bash
python main.py --dashboard
```

Then:
- Open http://localhost:7860 in your browser
- Upload a CSV or Excel file
- Click "🚀 Run AI Analysis"
- Explore the three tabs: BI Dashboard, ML Dashboard, AI Insights

#### Option C: Command Line Analysis
```bash
python main.py --analyze your_data.csv
```

---

### Step 3: Try Sample Datasets

The examples create sample datasets in `data/`:
- `sample_loan_data.csv` - Regression (loan amount prediction)
- `sample_churn_data.csv` - Classification (customer churn)

Upload these in the dashboard to see the system in action!

---

## 📊 What to Expect

### After Upload & Analysis:

**BI Dashboard Tab:**
- ✅ Automatic target detection
- ✅ Feature correlation rankings
- ✅ 6 intelligently selected visualizations
- ✅ Correlation matrix heatmap

**ML Dashboard Tab:**
- ✅ Best model selected (from 6-8 candidates)
- ✅ Performance metrics and comparison
- ✅ Feature importance rankings
- ✅ Hyperparameter details
- ✅ Clear reasoning for model selection

**AI Insights Tab:**
- ✅ Executive summary
- ✅ Model selection insights
- ✅ Top 5 feature deep-dives
- ✅ Strategic recommendations
- ✅ Downloadable Markdown report

---

## 🎯 Your First Analysis

### Example: Analyzing Sales Data

1. **Prepare your data**
   - CSV or Excel format
   - One row per observation
   - Mix of numeric and categorical columns
   - Target column (or let AI detect it)

2. **Run analysis**
   ```bash
   python main.py --dashboard
   ```

3. **Upload file**
   - Click "📁 Upload Dataset"
   - Select your file
   - Optionally specify target column
   - Click "🚀 Run AI Analysis"

4. **Wait 30-120 seconds**
   - Target detection: ~5s
   - Correlation analysis: ~10s
   - Graph selection: ~5s
   - AutoML training: ~30-90s (depends on dataset size)
   - Insight generation: ~5s

5. **Explore results**
   - Navigate between tabs
   - Interact with visualizations
   - Read AI-generated insights
   - Download report

---

## 🔧 Common Customizations

### Change Dashboard Port
```bash
python main.py --dashboard --port 8080
```

### Specify Target Column
In the dashboard: Enter column name in "🎯 Target Column" field

Or via command line:
```bash
python main.py --analyze data.csv --target price
```

### Create Public Share Link
```bash
python main.py --dashboard --share
```

### Adjust AutoML Settings
Edit `config/settings.py`:
```python
automl_config.n_trials = 100  # More trials = better optimization
automl_config.cv_folds = 10   # More folds = better validation
```

---

## 🐛 Troubleshooting

**"Port already in use"**
```bash
python main.py --dashboard --port 8080
```

**"Out of memory"**
- Reduce dataset size: `data_config.max_rows = 50000`
- Enable sampling: `data_config.enable_sampling = True`

**"No target detected"**
- Specify manually in dashboard
- Or: `python main.py --analyze data.csv --target your_column`

**"Installation failed"**
```bash
# Install one by one if bulk install fails
pip install pandas numpy scipy --break-system-packages
pip install plotly gradio --break-system-packages
pip install scikit-learn xgboost lightgbm catboost --break-system-packages
pip install optuna --break-system-packages
```

---

## 📚 Next Steps

1. **Read full documentation**: `README.md`
2. **Explore configuration**: `config/settings.py`
3. **Check example code**: `examples.py`
4. **Try your own data**: Any CSV/Excel file
5. **Customize for your needs**: Modify engines and settings

---

## 💡 Pro Tips

### Faster Analysis
- Use smaller `n_trials` for quick experiments (default: 50)
- Reduce `cv_folds` for speed (default: 5)
- Enable sampling for large datasets

### Better Models
- Increase `n_trials` to 100+ for important analyses
- Use `cv_folds = 10` for robust validation
- Let optimization run longer: `optimization_timeout_seconds = 600`

### Better Insights
- Provide descriptive column names
- Clean data before upload (handle obvious errors)
- Use domain knowledge to verify target detection
- Read the "Why This Model?" section in ML Dashboard

### Production Deployment
- Save best model: Results are cached in `cache/`
- Export insights: Use download button
- Retrain periodically: Upload new data regularly
- Monitor performance: Check logs in `logs/`

---

## 🎓 Learning Resources

### Understanding Results

**Correlation Coefficient (r):**
- -1 to +1 range
- Positive: Variables increase together
- Negative: One increases, other decreases
- Closer to ±1: Stronger relationship

**P-value:**
- < 0.05: Statistically significant
- < 0.01: Highly significant
- < 0.001: Very highly significant

**R² Score (Regression):**
- 0 to 1 range
- 0.7+: Good model
- 0.8+: Very good model
- 0.9+: Excellent model

**ROC-AUC (Classification):**
- 0.5: Random guess
- 0.7+: Acceptable
- 0.8+: Good
- 0.9+: Excellent

### Models Explained

**Random Forest:** Ensemble of decision trees, robust and interpretable
**XGBoost:** Gradient boosting, excellent for structured data
**LightGBM:** Fast gradient boosting, good for large datasets
**CatBoost:** Handles categorical features well, less tuning needed
**Logistic/Linear:** Simple, fast, good baseline

---

## ✅ You're Ready!

Now you have everything you need to start using the AI BI Desktop Application.

**Quick Recap:**
```bash
# 1. Install
pip install -r requirements.txt --break-system-packages

# 2. Run examples OR launch dashboard
python examples.py
# OR
python main.py --dashboard

# 3. Upload data and explore!
```

**Questions?** Check `README.md` for detailed documentation.

**Issues?** Review troubleshooting section above.

**Ready for more?** Explore advanced configuration in `config/settings.py`.

---

🎉 **Happy Analyzing!**
