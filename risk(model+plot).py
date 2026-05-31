# =========================
# 1. Import Libraries
# =========================
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# =========================
# 2. Load Dataset
# =========================
df = pd.read_csv("loan_risk_dataset.csv")

print(df.head())
print(df.info())

# =========================
# 3. Check Missing Values
# =========================
print(df.isnull().sum())

df = df.dropna()

# =========================
# 4. Exploratory Data Analysis (EDA)
# =========================

# توزيع القبول/الرفض
sns.countplot(x="approved", data=df)
plt.title("Loan Approval Distribution")
plt.show()

# تأثير العمر
sns.boxplot(x="approved", y="age", data=df)
plt.title("Age vs Approval")
plt.show()

# تأثير الراتب
sns.boxplot(x="approved", y="salary", data=df)
plt.title("Salary vs Approval")
plt.show()

# تأثير الديون
sns.boxplot(x="approved", y="debt", data=df)
plt.title("Debt vs Approval")
plt.show()

# correlation heatmap
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# =========================
# 5. Features & Target
# =========================

X = df[[
    "age",
    "salary",
    "debt",
    "loans_count",
    "work_years"
]]

y = df["approved"]

# =========================
# 6. Train/Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 7. Feature Scaling
# =========================

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =========================
# 8. Models
# =========================

# Logistic Regression
lr_model = LogisticRegression()
lr_model.fit(X_train_scaled, y_train)

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# =========================
# 9. Predictions
# =========================

lr_pred = lr_model.predict(X_test_scaled)
rf_pred = rf_model.predict(X_test)

# =========================
# 10. Evaluation
# =========================

print("🔹 Logistic Regression")
print("Accuracy:", accuracy_score(y_test, lr_pred))
print(classification_report(y_test, lr_pred))
print(confusion_matrix(y_test, lr_pred))

print("\n========================\n")

print("🔹 Random Forest")
print("Accuracy:", accuracy_score(y_test, rf_pred))
print(classification_report(y_test, rf_pred))
print(confusion_matrix(y_test, rf_pred))

# =========================
# 11. Feature Importance
# =========================

importances = rf_model.feature_importances_
features = X.columns

feat_imp = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print(feat_imp)

plt.figure(figsize=(8,5))
sns.barplot(x="Importance", y="Feature", data=feat_imp)
plt.title("Feature Importance (Random Forest)")
plt.show()

# =========================
# 12. Predict New Customer
# =========================

# ترتيب الإدخال مهم جداً:
# age, salary, debt, loans_count, work_years

new_customer = np.array([[35, 5000, 2000, 1, 10]])

new_customer_scaled = scaler.transform(new_customer)

prediction = lr_model.predict(new_customer_scaled)

print("Prediction:",
      "Approved" if prediction[0] == 1 else "Rejected")
      
