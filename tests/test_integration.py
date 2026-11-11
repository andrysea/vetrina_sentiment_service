
import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient

from app.main import app
from app.services import predicts


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# TEST 1 - Verifica delle predizioni reali del modello
@pytest.mark.parametrize(
    "review, expected_sentiment",
    [
        ("This product is amazing!", "positive"),
        ("This product is terrible!", "negative"),
    ]
)
def test_predict_real_model(client, review, expected_sentiment):
    response = client.post(
        "/predict",
        json={"review": review}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sentiment"] == expected_sentiment
    assert 0 <= data["confidence"] <= 1


# TEST 2 - Verifica del rifiuto delle recensioni non valide
@pytest.mark.parametrize(
    "review",
    ["", "   ", 123, "a" * 5001]
)
def test_predict_invalid_review(client, review):
    response = client.post(
        "/predict",
        json={"review": review}
    )

    assert response.status_code == 422


# TEST 3 - Verifica della gestione degli errori interni
def test_predict_internal_error(client, monkeypatch):
    fake_predict = Mock(
        side_effect=RuntimeError("Internal model failure")
    )

    monkeypatch.setattr(
        predicts,
        "predict_sentiment",
        fake_predict
    )

    response = client.post(
        "/predict",
        json={"review": "Amazing product!"}
    )

    assert response.status_code == 500
    assert "Internal model failure" not in str(response.json())


# TEST 4 - Verifica dell'esposizione delle metriche Prometheus
def test_metrics_endpoint(client):
    client.post(
        "/predict",
        json={"review": "Amazing product!"}
    )

    response = client.get("/metrics")

    assert response.status_code == 200

    metrics = response.text

    assert "sentiment_prediction_errors_total" in metrics
    assert "sentiment_request_duration_seconds_count" in metrics
    assert 'endpoint="/predict"' in metrics


# Funzione di supporto - Lettura del contatore degli errori
def get_error_count(client):
    response = client.get("/metrics")
    assert response.status_code == 200

    for line in response.text.splitlines():
        if line.startswith("sentiment_prediction_errors_total "):
            return float(line.split()[-1])

    raise AssertionError("Metrica errori non trovata")


# TEST 5 - Verifica dell'incremento del contatore degli errori
def test_prediction_error_counter(client, monkeypatch):
    before = get_error_count(client)

    monkeypatch.setattr(
        predicts,
        "predict_sentiment",
        Mock(side_effect=RuntimeError("Model failure"))
    )

    response = client.post(
        "/predict",
        json={"review": "Test product"}
    )

    after = get_error_count(client)

    assert response.status_code == 500
    assert after == before + 1
