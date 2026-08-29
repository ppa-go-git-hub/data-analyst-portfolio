from fastapi import APIRouter, Query, Body, File, UploadFile
from pydantic import BaseModel, Field, create_model
from typing import Literal
from io import StringIO
import pandas as pd

from .core import FEATURES, PIPELINES, predict, predict_proba

ModelLiteral = Literal[*PIPELINES]

BanknoteModel = create_model("Banknote", **{ feature: (float, Field(default=None, ge=0)) for feature in FEATURES })

router = APIRouter()

@router.get("/", tags=["General"])
async def root():
    """Page d'accueil"""
    return {
        "message": "Bienvenue dans l'API de détection automatique de faux billets",
    }

@router.get("/health", tags=["Monitoring"])
async def health():
    """Pour vérifier si tout fonctionne"""
    return {
        "status": "online",
        "version": "0.0.1",
        "pipelines": {
            name: { "isAvailable": model is not None }
            for name, model in PIPELINES.items()
        },
    }

def results_json(X, y, proba):
    for x, is_fake, (proba_genuine, proba_fake) in zip(X.to_numpy(), y, proba):
        yield {
            "prediction": ("fake" if is_fake else "genuine"),
            "isGenuine": not is_fake,
            "probaGenuine": round(proba_genuine, 3),
            "probaFake": round(proba_fake, 3),
            "nMissingFeatures": x.tolist().count(None),
        }

@router.post("/predict/single", tags=["Prediction"])
async def predict_single(
    model: ModelLiteral = Query(...),
    banknote: BanknoteModel = Body(...),
):
    """Prédiction pour un seul billet"""
    banknote_dict = banknote.model_dump()
    single = [ banknote_dict.get(feature, None) for feature in FEATURES ]
    X = pd.DataFrame([ single ], columns=FEATURES)
    y = predict(model, X)
    proba = predict_proba(model, X)
    return {
        "model": model,
        "results": list(results_json(X, y, proba)),
    }

@router.post("/predict/csv", tags=["Prediction"])
async def predict_csv(
    model: ModelLiteral = Query(...),
    csv_file: UploadFile = File(...),
):
    """Prédiction pour plusieurs billets à partir d'un fichier CSV"""
    csv_contents = await csv_file.read()
    df_csv = pd.read_csv(StringIO(csv_contents.decode("utf-8")))
    X = df_csv[[*FEATURES]]
    y = predict(model, X)
    proba = predict_proba(model, X)
    return {
        "model": model,
        "results": list(results_json(X, y, proba)),
    }
