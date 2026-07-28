from openai import OpenAI

from app.config.settings import settings
from app.models.request import RFQRequest
from app.models.result import RFQExtractionResult
from app.models.rfq import RFQExtraction
from app.prompts.extraction import EXTRACTION_SYSTEM_PROMPT
# from app.services.validator import RFQValidator


class RFQExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        # self.validator = RFQValidator()

    def extract(self, request: RFQRequest) -> RFQExtractionResult:
        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": EXTRACTION_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": request.email_body,
                },
            ],
            text_format=RFQExtraction,
        )

        extracted = response.output_parsed

        # return self.validator.validate(extracted)
        return response.output_parsed