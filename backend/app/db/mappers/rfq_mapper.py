from app.db.models.rfq import RFQDB
from app.models.result import RFQExtractionResult


class RFQMapper:

    @staticmethod
    def to_db(
        email: str,
        result: RFQExtractionResult,
    ) -> RFQDB:

        rfq = result.extracted_data

        return RFQDB(
            original_email=email,
            project_name=rfq.project_name,
            client_name=rfq.client,
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