import pandas as pd

# Load model
import joblib
model = joblib.load('/Users/shryqb/PycharmProjects/ai_bi_desktop/cache/train_analysis.pkl')
print(type(model))
# Load test data
tst = '/Users/shryqb/Downloads/stock-pledge-financing-default-prediction-2026/test.csv'
test = pd.read_csv(tst)

target = 'IsDefault'

# Prepare test data
if target in test.columns:
    X_test = test.drop(columns=[target])
else:
    X_test = test.copy()

print(X_test.dtypes)

# Predict
X_test["Stock code"] = X_test["Stock code"].astype("category")
predictions = model.best_model.model.predict(X_test)

# Add predictions
test[target] = predictions

# Optional – probability
if hasattr(model, "predict_proba"):
    test['default_probability'] = model.predict_proba(X_test)[:, 1]

# Save
final = test[['Stock code',target]]
final.to_csv('test_with_predictions.csv', index=False)
