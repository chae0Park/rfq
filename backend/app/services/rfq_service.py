from app.models.request import RFQRequest
from app.models.result import RFQExtractionResult
from app.services.extractor import RFQExtractor
from app.services.validator import RFQValidator

from sqlalchemy.orm import Session

from app.db.repositories.rfq_repository import RFQRepository
from app.enums.rfq_status import RFQStatus


class RFQService:
    def __init__(self, db: Session):
        self.extractor = RFQExtractor()
        self.validator = RFQValidator()
        self.repository = RFQRepository(db)

    def process_email(
        self,
        request: RFQRequest,
    ) -> RFQExtractionResult:

        # 1. Extract RFQ information with GPT
        extraction = self.extractor.extract(request)

        # 2. Validate required fields
        validation = self.validator.validate(extraction)

        # 3. Save RFQ to DB
        saved_rfq = self.repository.create(
            request=request,
            result=validation,
        )

        # 4. Update RFQ status
        self.repository.update_status(
            rfq=saved_rfq,
            status=RFQStatus.VALIDATED,
        )

        # 5. Return extraction + validation + generated RFQ ID
        return RFQExtractionResult(
            rfq_id=saved_rfq.id,
            extracted_data=validation.extracted_data,
            missing_fields=validation.missing_fields,
            clarification_questions=validation.clarification_questions,
            ready_for_quotation=validation.ready_for_quotation,
        )