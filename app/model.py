import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model():

    df = pd.read_csv("data/student_data.csv")

    X = df.drop("performance", axis=1)
    y = df["performance"]

    model = RandomForestClassifier()
    model.fit(X, y)

    os.makedirs("trained_model", exist_ok=True)
    joblib.dump(model, "trained_model/model.pkl")

    print("Model trained successfully!")