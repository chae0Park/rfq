from app.models.request import RFQRequest
from app.models.result import RFQExtractionResult
from app.services.extractor import RFQExtractor
from app.services.validator import RFQValidator
from app.db.repositories.llm_call_log_repository import LLMCallLogRepository

from sqlalchemy.orm import Session

from app.db.repositories.rfq_repository import RFQRepository
from app.enums.rfq_status import RFQStatus
from app.config.settings import settings
from app.utils.llm_cost import calculate_llm_cost


class RFQService:
    def __init__(self, db: Session):
        self.extractor = RFQExtractor()
        self.validator = RFQValidator()
        self.repository = RFQRepository(db)
        self.llm_log_repository = LLMCallLogRepository(db)

    def process_email(
        self,
        request: RFQRequest,
    ) -> RFQExtractionResult:

        # 1. Extract RFQ information with GPT
        try:
            extraction_result = self.extractor.extract(request)

        except Exception as error:
            self.llm_log_repository.create(
                rfq_id=None,
                task_type="RFQ_EXTRACTION",
                model=settings.OPENAI_MODEL,
                status="FAILED",
                latency_ms=None,
                input_tokens=None,
                output_tokens=None,
                estimated_cost=None,
                error_message=str(error),
            )

            raise

        extraction = extraction_result["extraction"]

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

        # 5. Successful LLM call log
        self.llm_log_repository.create(
            rfq_id=saved_rfq.id,
            task_type="RFQ_EXTRACTION",
            model=settings.OPENAI_MODEL,
            status="SUCCESS",
            latency_ms=extraction_result["latency_ms"],
            input_tokens=extraction_result["input_tokens"],
            output_tokens=extraction_result["output_tokens"],
            estimated_cost=calculate_llm_cost(
                extraction_result["input_tokens"],
                extraction_result["output_tokens"],
            ),
            error_message=None,
        )

        # 6. Return result
        return RFQExtractionResult(
            rfq_id=saved_rfq.id,
            extracted_data=validation.extracted_data,
            missing_fields=validation.missing_fields,
            clarification_questions=validation.clarification_questions,
            ready_for_quotation=validation.ready_for_quotation,
        )