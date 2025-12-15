import joblib
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "saved_model", "model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "..", "saved_model", "features.pkl")

_model = None
_features = None

def load_model():
    global _model, _features
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _features is None:
        _features = joblib.load(FEATURE_PATH)
    return _model, _features

def preprocess_input(data: dict):
    """
    Input JSON harus:
    {
        "sex": "M",
        "length": 0.455,
        "diameter": 0.365,
        "height": 0.095,
        "whole_weight": 0.514,
        "shucked_weight": 0.2245,
        "viscera_weight": 0.101,
        "shell_weight": 0.15
    }
    """

    raw_df = pd.DataFrame([[
        data["sex"],
        data["length"],
        data["diameter"],
        data["height"],
        data["whole_weight"],
        data["shucked_weight"],
        data["viscera_weight"],
        data["shell_weight"],
    ]], columns=[0, 1, 2, 3, 4, 5, 6, 7])  

    df = pd.get_dummies(raw_df, columns=[0], prefix="Sex")

    model, feature_cols = load_model()

    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_cols]

    return df.values

def predict(data: dict):
    model, _ = load_model()
    X = preprocess_input(data)
    pred = model.predict(X)[0]
    return float(pred)
