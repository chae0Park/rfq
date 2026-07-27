from app.models.result import PriceReviewResult

class PriceReviewService:

    def review(
        self,
        rfq,
        quotation,
    ) -> PriceReviewResult:
        ...