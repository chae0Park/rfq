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
from app.db.mappers.rfq_mapper import RFQMapper


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

        # 1. Check whether this email belongs to an existing RFQ thread
        existing_rfq = None

        if request.thread_id:
            existing_rfq = self.repository.get_by_thread_id(
                request.thread_id
            )

        is_clarification_reply = (
            existing_rfq is not None
            and existing_rfq.status == RFQStatus.WAITING_FOR_CLIENT
        )

        # 2. Extract RFQ information with GPT
        try:
            extraction_result = self.extractor.extract(request)

        except Exception as error:
            self.llm_log_repository.create(
                rfq_id=existing_rfq.id if is_clarification_reply else None,
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

        # 3. Clarification reply → merge with existing RFQ
        if is_clarification_reply:
            existing_extraction = RFQMapper.to_extraction(existing_rfq)

            extraction = RFQMapper.merge_extractions(
                existing=existing_extraction,
                incoming=extraction,
            )

        # 4. Validate required fields
        validation = self.validator.validate(extraction)

        # 5. Save new RFQ or update existing RFQ
        if is_clarification_reply:
            update_data = validation.extracted_data.model_dump()

            update_data.update({
                "missing_fields": validation.missing_fields,
                "clarification_questions": validation.clarification_questions,
                "ready_for_quotation": validation.ready_for_quotation,
                "gmail_message_id": request.message_id,
            })

            saved_rfq = self.repository.update(
                rfq=existing_rfq,
                update_data=update_data,
            )

        else:
            saved_rfq = self.repository.create(
                request=request,
                result=validation,
            )

        # 6. Update RFQ status
        new_status = (
            RFQStatus.READY_FOR_QUOTATION
            if validation.ready_for_quotation
            else RFQStatus.CLARIFICATION_REQUIRED
        )

        self.repository.update_status(
            rfq=saved_rfq,
            status=new_status,
        )

        # 7. Successful LLM call log
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

        # 8. Return result
        return RFQExtractionResult(
            rfq_id=saved_rfq.id,
            extracted_data=validation.extracted_data,
            missing_fields=validation.missing_fields,
            clarification_questions=validation.clarification_questions,
            ready_for_quotation=validation.ready_for_quotation,
        )

    def mark_waiting_for_client(self, rfq_id: int):
        rfq = self.repository.get_by_id(rfq_id)

        if rfq is None:
            raise ValueError(f"RFQ {rfq_id} not found")

        return self.repository.update_status(
            rfq=rfq,
            status=RFQStatus.WAITING_FOR_CLIENT,
        )

    def get_by_thread_id(self, thread_id: str):
        return self.repository.get_by_thread_id(thread_id)