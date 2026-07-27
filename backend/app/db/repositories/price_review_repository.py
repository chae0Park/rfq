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
            recommendation=result.recommendation,
            confidence=result.confidence,
            summary=result.summary,
        )

        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        return review