from pydantic import BaseModel

class PriceReviewResult(BaseModel):
    status: str
    price: float
    benchmark_low: float | None = None
    benchmark_high: float | None = None
    source_type: str | None = None