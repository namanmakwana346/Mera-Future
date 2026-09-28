# --------------------------------------------------
# READINESS SCORE MODEL - TRAINING SCRIPT
# Yeh script SIRF EK BAAR chalani hai (terminal mein)
# Isse "readiness_model.pkl" file ban jayegi
# --------------------------------------------------

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pickle

# Apni CSV file ka sahi naam yahan daalein
df = pd.read_csv("student.csv")

# Features (yeh factors readiness_score predict karne mein use honge)
X = df[['cgpa', 'technical_score', 'projects_completed',
        'github_projects', 'internship_months']]
y = df['readiness_score']

# Train-test split (model ko test karne ke liye data alag rakha)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model train karna
model = LinearRegression()
model.fit(X_train, y_train)

# Model kitna accurate hai, check karna
predictions = model.predict(X_test)
accuracy = r2_score(y_test, predictions)

print(f"Model trained successfully!")
print(f"Accuracy (R2 Score): {accuracy:.2f}")
print()
print("Feature Importance (coefficients):")
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature}: {coef:.3f}")

# Model ko file mein save karna, taaki baar baar train na karna pade
with open("readiness_model.pkl", "wb") as f:
    pickle.dump(model, f)

print()
print("Model 'readiness_model.pkl' file mein save ho gaya!")
