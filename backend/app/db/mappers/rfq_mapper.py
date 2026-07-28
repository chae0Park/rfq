from app.db.models.rfq import RFQDB
from app.models.result import RFQExtractionResult
from app.models.request import RFQRequest


class RFQMapper:

    @staticmethod
    def to_db(
        request: RFQRequest,
        result: RFQExtractionResult,
    ) -> RFQDB:

        rfq = result.extracted_data

        return RFQDB(
            original_email=request.email_body,

            client_name=request.from_name,
            client_email=request.from_email,

            project_name=rfq.project_name,
            client=rfq.client,          # RFQ에서 추출된 회사명
            country=rfq.country,
            countries=rfq.countries,
            sample_size=rfq.sample_size,
            loi=rfq.loi,
            ir=rfq.ir,
            methodology=rfq.methodology,
            timeline=rfq.timeline,
            languages=rfq.languages,
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