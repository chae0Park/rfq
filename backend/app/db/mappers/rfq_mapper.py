from app.db.models.rfq import RFQDB
from app.models.result import RFQExtractionResult
from app.models.request import RFQRequest
from app.models.rfq import RFQExtraction


class RFQMapper:

    @staticmethod
    def to_db(
        request: RFQRequest,
        result: RFQExtractionResult,
    ) -> RFQDB:

        rfq = result.extracted_data

        return RFQDB(
            original_email=request.email_body,

            gmail_thread_id=request.thread_id,
            gmail_message_id=request.message_id,

            client_name=request.from_name,
            client_email=request.from_email,

            project_name=rfq.project_name,
            client=rfq.client,        

            country=rfq.country,
            countries=rfq.countries,
            region=rfq.region,
            city=rfq.city,

            target_audience=rfq.target_audience,
            gender=rfq.gender,
            age=rfq.age,
            quota=rfq.quota,

            sample_size=rfq.sample_size,
            loi=rfq.loi,
            ir=rfq.ir,

            methodology=rfq.methodology,
            timeline=rfq.timeline,
            languages=rfq.languages,

            project_scope=rfq.project_scope,
            end_client=rfq.end_client,
            additional_notes=rfq.additional_notes,

            programming_required=rfq.programming_required,
            translation_required=rfq.translation_required,
            overlay_required=rfq.overlay_required,

            rush=rfq.rush,
            client_tier=rfq.client_tier,
            currency=rfq.currency,
            
            missing_fields=result.missing_fields,
            clarification_questions=result.clarification_questions,
            ready_for_quotation=result.ready_for_quotation,
        )

    @staticmethod
    def to_extraction(rfq: RFQDB) -> RFQExtraction:
        return RFQExtraction(
            project_name=rfq.project_name,
            country=rfq.country,
            countries=rfq.countries,
            region=rfq.region,
            city=rfq.city,
            sample_size=rfq.sample_size,
            target_audience=rfq.target_audience,
            gender=rfq.gender,
            age=rfq.age,
            quota=rfq.quota,
            timeline=rfq.timeline,
            methodology=rfq.methodology,
            translation_required=rfq.translation_required,
            programming_required=rfq.programming_required,
            overlay_required=rfq.overlay_required,
            project_scope=rfq.project_scope,
            loi=rfq.loi,
            ir=rfq.ir,
            languages=rfq.languages,
            client=rfq.client,
            end_client=rfq.end_client,
            additional_notes=rfq.additional_notes,
            rush=rfq.rush,
            client_tier=rfq.client_tier,
            currency=rfq.currency,
        )

    @staticmethod
    def merge_extractions(
        existing: RFQExtraction,
        incoming: RFQExtraction,
    ) -> RFQExtraction:

        existing_data = existing.model_dump()
        incoming_data = incoming.model_dump(exclude_none=True)

        for field, value in incoming_data.items():
            existing_data[field] = value

        return RFQExtraction(**existing_data)