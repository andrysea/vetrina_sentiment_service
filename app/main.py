from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.services.sentiments import load_model
from app.services import metrics, predicts
from app.services.metrics import measure_request

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    yield

app = FastAPI(
    title="Vetrinia Sentiment Analysis API",
    version="1.0.0",
    lifespan=lifespan
)
app.middleware("http")(measure_request) # Stiamo dicendo a FastAPI, ogni volta che ricevi una richiesta HTTP esegui il middleware

# Qui diciamo a FastAPI di includere gli endpoint definiti nei moduli
app.include_router(predicts.router)
app.include_router(metrics.router)