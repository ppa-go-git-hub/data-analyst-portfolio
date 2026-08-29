import pandas as pd
import sklearn
import joblib
from pathlib import Path

sklearn.set_config(transform_output="pandas")

FEATURES = ("diagonal", "height_left", "height_right", "margin_low", "margin_up", "length")
TARGET = "is_fake"

API_PATH = Path(__file__).resolve().parent
PIPELINES_PATH = API_PATH.parent.parent / "data" / "pipelines"

def load_pipeline(name):
    try:
        return joblib.load(PIPELINES_PATH / f"{name}.joblib")
    except:
        pass

PIPELINES = { name: load_pipeline(name) for name in ("lr", "knn", "rf") }

def predict(model, X):
    pipeline = PIPELINES.get(model, None)
    assert pipeline is not None
    return pipeline.predict(X)

def predict_proba(model, X):
    pipeline = PIPELINES.get(model, None)
    assert pipeline is not None
    return pipeline.predict_proba(X)
