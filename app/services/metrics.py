from fastapi import APIRouter, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from time import perf_counter
from fastapi import Request
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

PREDICTION_ERRORS = Counter(
    "sentiment_prediction_errors_total",
    "Numero di errori durante le predizioni"
)

REQUEST_DURATION = Histogram(
    "sentiment_request_duration_seconds",
    "Tempo di risposta delle richieste HTTP",
    ["method", "endpoint", "status_code"]
)

# Creo il middleware
async def measure_request(request: Request, call_next):
    start = perf_counter()
    status_code = 500
    response = None

    try:
        # Inoltro richiesta a endpoint chiamato da utente e ottengo la risposta
        response = await call_next(request)
        
        # Recupero il codice HTTP della risposta
        status_code = response.status_code
        
        # Restituisci la risposta
        return response

    finally:
        duration = perf_counter() - start

        # Recupera la rotta
        route = request.scope.get("route")
        endpoint = route.path if route else "unmatched"

        # Registra la durata con REQUEST_DURATION 
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=status_code
        ).observe(duration)

@router.get("/metrics", include_in_schema=False)
def get_metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )