from fastapi import APIRouter, Request
from app.schemas.PredictionResponse import PredictionResponse
from app.schemas.ReviewRequest import ReviewRequest
from app.services.metrics import PREDICTION_ERRORS
from app.services.sentiments import predict_sentiment
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def sentiment_response(review: ReviewRequest, request: Request):
    try:
        model = request.app.state.model
        return predict_sentiment(model, review.review)
    except ValueError as exc:
        logger.exception("ERROR - Dati non validi.")
        raise HTTPException(
            status_code=500,
            detail="Dati inseriti non validi."
        ) from exc
    except Exception as exc:
        PREDICTION_ERRORS.inc()
        logger.exception("ERROR - Errore imprevisto generico.")
        raise HTTPException(
            status_code=500,
            detail="Errore imprevisto generico."
        ) from exc
