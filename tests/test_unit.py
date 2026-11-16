import pytest
from pydantic import ValidationError
from app.schemas.PredictionResponse import PredictionResponse
from app.schemas.ReviewRequest import ReviewRequest
from unittest.mock import Mock
from app.services.sentiments import predict_sentiment

# TEST 1 - stringa inserita viene controllata e aggiornata
def test_review_valid():
    review = ReviewRequest(review="   Amazing product!   ")
    review_true = "Amazing product!"
    assert review.review == review_true

# TEST 2 - stringa inserita solo spazzi e eccezione sollevata
def test_review_spaces():
    with pytest.raises(ValidationError):
        ReviewRequest(review="   ")

# TEST 3 - stringa inserita vuota e eccezione sollevata
def test_review_blank():
    with pytest.raises(ValidationError):
        ReviewRequest(review="")

# TEST 4 - stringa lunghezza massima
def test_review_too_long():
    with pytest.raises(ValidationError):
        ReviewRequest(review="a" * 5001)

# TEST 5 - controllo inserimento valori corretti
def test_prediction_response_valid():
    response = PredictionResponse(
        sentiment="positive",
        confidence=0.85
    )
    assert response.sentiment == "positive"
    assert response.confidence == 0.85

# TEST 6 - controllo inserimento valore non corretto di confidence
def test_prediction_confidence_not_valid():
    with pytest.raises(ValidationError):
        PredictionResponse(
            sentiment="positive",
            confidence=1.5
        )

# TEST 7 - controllo inserimento valore non corretto di sentiment
def test_prediction_sentiment_not_valid():
    with pytest.raises(ValidationError):
        PredictionResponse(
            sentiment="happy",
            confidence=1.0
        )

# TEST 8 - verifica modello
def test_predict_sentiment():
    model = Mock()

    model.classes_ = ["negative", "neutral", "positive"]
    model.predict.return_value = ["positive"]
    model.predict_proba.return_value = [[0.1, 0.2, 0.7]]

    result = predict_sentiment(model, "Amazing product!")

    assert result["sentiment"] == "positive"
    assert result["confidence"] == 0.7

    model.predict.assert_called_once_with(["Amazing product!"])

# TEST 9 - modello senza probabilità
def test_predict_without_confidence():
    model = Mock(spec=["predict"])
    model.predict.return_value = ["negative"]

    result = predict_sentiment(model, "Terrible product!")

    assert result["sentiment"] == "negative"
    assert "confidence" not in result

# TEST 10 — Confidence opzionale
def test_prediction_response_without_confidence():
    response = PredictionResponse(sentiment="neutral")
    assert response.sentiment == "neutral"
    assert response.confidence is None

# TEST 11 — Lunghezza massima consentita
def test_review_max_length_valid():
    review = ReviewRequest(review="a" * 5000)
    assert len(review.review) == 5000