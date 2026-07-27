from app.models.rfq import RFQExtraction
from app.models.result import RFQExtractionResult
from app.services.clarification import ClarificationGenerator


class RFQValidator:
    """
    Validates whether an extracted RFQ contains the minimum
    information required to proceed with quotation.
    """

    REQUIRED_FIELDS = [
        "country",
        "sample_size",
        "target_audience",
        "timeline",
        "methodology",
    ]

    def validate(self, extraction: RFQExtraction) -> RFQExtractionResult:
        missing_fields = []

        for field in self.REQUIRED_FIELDS:
            value = getattr(extraction, field)

            if value is None:
                missing_fields.append(field)

        clarification_generator = ClarificationGenerator()

        questions = clarification_generator.generate(missing_fields)

        return RFQExtractionResult(
            extracted_data=extraction,
            missing_fields=missing_fields,
            clarification_questions=questions,
            ready_for_quotation=len(missing_fields) == 0,
        )