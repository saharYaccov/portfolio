"""
Example Usage Script
===================
Demonstrates how to use the AI BI Desktop Application
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import quick_analyze
from ui.gradio_app import launch_dashboard


def create_sample_regression_dataset():
    """
    Create a sample regression dataset for testing
    """
    np.random.seed(42)
    n_samples = 1000
    
    # Features
    age = np.random.randint(18, 80, n_samples)
    income = np.random.normal(50000, 20000, n_samples)
    credit_score = np.random.randint(300, 850, n_samples)
    years_employed = np.random.randint(0, 40, n_samples)
    
    # Categorical features
    education = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples, 
                                 p=[0.3, 0.4, 0.2, 0.1])
    employment_type = np.random.choice(['Full-time', 'Part-time', 'Self-employed', 'Unemployed'], 
                                       n_samples, p=[0.6, 0.2, 0.15, 0.05])
    
    # Target: Loan amount (with realistic relationships)
    loan_amount = (
        income * 0.3 +
        credit_score * 50 +
        years_employed * 1000 +
        np.random.normal(0, 5000, n_samples)
    )
    loan_amount = np.maximum(loan_amount, 5000)  # Minimum loan
    
    # Create DataFrame
    df = pd.DataFrame({
        'age': age,
        'annual_income': income,
        'credit_score': credit_score,
        'years_employed': years_employed,
        'education_level': education,
        'employment_type': employment_type,
        'requested_loan_amount': loan_amount
    })
    
    return df


def create_sample_classification_dataset():
    """
    Create a sample classification dataset (customer churn)
    """
    np.random.seed(42)
    n_samples = 1000
    
    # Features
    tenure_months = np.random.randint(1, 72, n_samples)
    monthly_charges = np.random.normal(70, 30, n_samples)
    total_charges = tenure_months * monthly_charges + np.random.normal(0, 500, n_samples)
    
    # Service features
    internet_service = np.random.choice(['DSL', 'Fiber', 'No'], n_samples, p=[0.4, 0.4, 0.2])
    contract_type = np.random.choice(['Month-to-month', 'One year', 'Two year'], 
                                     n_samples, p=[0.5, 0.3, 0.2])
    payment_method = np.random.choice(['Electronic', 'Mailed check', 'Bank transfer', 'Credit card'],
                                      n_samples, p=[0.3, 0.25, 0.25, 0.2])
    
    # Support tickets
    support_tickets = np.random.poisson(2, n_samples)
    
    # Target: Churn (with realistic relationships)
    churn_prob = (
        0.7 * (tenure_months < 12) +  # New customers churn more
        0.5 * (monthly_charges > 100) +  # High charges increase churn
        0.3 * (contract_type == 'Month-to-month') +
        0.2 * (support_tickets > 3) +
        np.random.normal(0, 0.2, n_samples)
    )
    
    churn = (churn_prob > 0.5).astype(int)
    churn_label = ['No', 'Yes']
    churn = [churn_label[c] for c in churn]
    
    # Create DataFrame
    df = pd.DataFrame({
        'tenure_months': tenure_months,
        'monthly_charges': monthly_charges,
        'total_charges': total_charges,
        'internet_service': internet_service,
        'contract_type': contract_type,
        'payment_method': payment_method,
        'support_tickets': support_tickets,
        'customer_churn': churn  # Target column
    })
    
    return df


def example_1_regression():
    """
    Example 1: Regression analysis with automatic target detection
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Regression Analysis (Loan Amount Prediction)")
    print("=" * 70)
    
    # Create sample data
    df = create_sample_regression_dataset()
    
    # Save to file
    file_path = 'data/sample_loan_data.csv'
    Path('data').mkdir(exist_ok=True)
    df.to_csv(file_path, index=False)
    
    print(f"\n✓ Created sample dataset: {file_path}")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    print(f"\nColumns:")
    for col in df.columns:
        print(f"  - {col}")
    
    # Run analysis
    print("\n🚀 Running automated analysis...")
    result = quick_analyze(file_path)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\n📊 Target Detected: {result.selected_target.column_name}")
    print(f"   Confidence: {result.selected_target.confidence_score:.2%}")
    print(f"   Task Type: {result.selected_target.task_type}")
    
    print(f"\n🤖 Best Model: {result.best_model.model_name}")
    print(f"   R² Score: {result.best_model.mean_cv_score:.4f}")
    
    print(f"\n🔥 Top 5 Predictive Features:")
    for i, corr in enumerate(result.correlations[:5], 1):
        print(f"   {i}. {corr.feature_name} (r={corr.correlation_value:.3f})")
    
    print(f"\n💡 Generated {len(result.insights)} AI-powered insights")
    
    print("\n" + "=" * 70)
    print("To view interactive dashboard:")
    print("  python main.py --dashboard")
    print("=" * 70 + "\n")


def example_2_classification():
    """
    Example 2: Classification analysis with manual target specification
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Binary Classification (Customer Churn Prediction)")
    print("=" * 70)
    
    # Create sample data
    df = create_sample_classification_dataset()
    
    # Save to file
    file_path = 'data/sample_churn_data.csv'
    Path('data').mkdir(exist_ok=True)
    df.to_csv(file_path, index=False)
    
    print(f"\n✓ Created sample dataset: {file_path}")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    
    # Run analysis with manual target
    print("\n🚀 Running automated analysis with target: customer_churn")
    result = quick_analyze(file_path, target_col='customer_churn')
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\n📊 Target: {result.selected_target.column_name}")
    print(f"   Task Type: {result.selected_target.task_type}")
    print(f"   Classes: {result.selected_target.n_unique}")
    
    print(f"\n🤖 Best Model: {result.best_model.model_name}")
    print(f"   ROC-AUC: {result.best_model.mean_cv_score:.4f}")
    
    print(f"\n🔥 Top Churn Indicators:")
    for i, corr in enumerate(result.correlations[:5], 1):
        direction = "↑" if corr.correlation_value > 0 else "↓"
        print(f"   {i}. {corr.feature_name} {direction} ({corr.test_type})")
    
    print(f"\n💡 Business Insights Generated: {len(result.insights)}")
    
    print("\n" + "=" * 70)


def example_3_dashboard():
    """
    Example 3: Launch interactive dashboard
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Interactive Dashboard")
    print("=" * 70)
    
    print("\n📊 Launching Gradio dashboard...")
    print("   Upload your own datasets or use the sample data created above")
    print("   Navigate between BI Dashboard, ML Dashboard, and AI Insights tabs")
    print("\n   Press Ctrl+C to quit\n")
    
    launch_dashboard(share=False, port=7860)


def main():
    """
    Run all examples
    """
    print("\n" + "=" * 70)
    print("AI BI DESKTOP APPLICATION - EXAMPLES")
    print("=" * 70)
    
    print("\nChoose an example:")
    print("  1. Regression Analysis (Loan Amount Prediction)")
    print("  2. Classification Analysis (Customer Churn)")
    print("  3. Launch Interactive Dashboard")
    print("  4. Run All Examples (1 & 2)")
    print("  0. Exit")
    
    choice = input("\nEnter choice (0-4): ").strip()
    
    if choice == '1':
        example_1_regression()
    elif choice == '2':
        example_2_classification()
    elif choice == '3':
        example_3_dashboard()
    elif choice == '4':
        example_1_regression()
        example_2_classification()
    elif choice == '0':
        print("Goodbye!")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
