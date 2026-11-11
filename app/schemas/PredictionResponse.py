
from typing import Literal
from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float | None = Field(default=None, ge=0, le=1)