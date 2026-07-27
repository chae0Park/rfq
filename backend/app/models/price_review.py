from pydantic import BaseModel


class PriceReviewResult(BaseModel):
    recommendation: str
    confidence: float
    summary: str