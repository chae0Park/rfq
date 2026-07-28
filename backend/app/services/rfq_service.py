from app.models.request import RFQRequest
from app.models.result import RFQExtractionResult
from app.services.extractor import RFQExtractor
from app.services.validator import RFQValidator
from sqlalchemy.orm import Session
from app.db.repositories.rfq_repository import RFQRepository
from app.enums.rfq_status import RFQStatus
from app.services.quotation_service import QuotationService
from app.services.price_review_service import PriceReviewService
from app.db.repositories.price_review_repository import PriceReviewRepository


class RFQService:
    def __init__(self,db: Session):
        self.extractor = RFQExtractor()
        self.validator = RFQValidator()
        self.repository = RFQRepository(db)
        self.quotation_service = QuotationService(db)
        self.price_review_service = PriceReviewService()
        self.price_review_repository = PriceReviewRepository(db)

    def process_email(
        self,
        request: RFQRequest,
    ) -> RFQExtractionResult:

        extraction = self.extractor.extract(request)

        validation = self.validator.validate(extraction)

        saved_rfq = self.repository.create(
            request=request,
            result=validation,
        )

        self.repository.update_status(
            rfq=saved_rfq,
            status=RFQStatus.VALIDATED,
        )

        print(validation.extracted_data.model_dump())

        quotation, saved_quotation = self.quotation_service.generate(
            rfq_id=saved_rfq.id,
            rfq=validation.extracted_data,
        )

        price_review = self.price_review_service.review(
            rfq=validation.extracted_data,
            quotation=quotation,
        )

        self.price_review_repository.create(
            rfq_id=saved_rfq.id,
            quotation_id=saved_quotation.id,   # DB 객체
            result=price_review,
        )

        print("Price review saved")

        print(price_review.model_dump())

        self.repository.update_status(
            rfq=saved_rfq,
            status=RFQStatus.PRICE_REVIEWED,
        )
        

        return validation