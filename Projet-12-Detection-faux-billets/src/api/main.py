from fastapi import FastAPI

from .router import router

app = FastAPI(
    title="API - Détection automatique de faux billets",
    description="Description de l'API",
    version="0.0.1",
)
app.include_router(router)
