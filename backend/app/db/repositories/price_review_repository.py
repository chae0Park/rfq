from sqlalchemy.orm import Session

from app.db.models.price_review import PriceReviewDB
from app.models.price_review import PriceReviewResult


class PriceReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        rfq_id: int,
        quotation_id: int,
        result: PriceReviewResult,
    ) -> PriceReviewDB:

        review = PriceReviewDB(
            rfq_id=rfq_id,
            quotation_id=quotation_id,
            status=result.status,
            price=result.price,
            benchmark_low=result.benchmark_low,
            benchmark_high=result.benchmark_high,
            source_type=result.source_type,
        )

        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        return review