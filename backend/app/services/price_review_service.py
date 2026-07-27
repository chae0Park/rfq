from openai import OpenAI

from app.config.settings import settings
from app.models.price_review import PriceReviewResult
from app.models.rfq import RFQExtraction
from app.models.quotation import QuotationResult


class PriceReviewService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def review(
        self,
        rfq: RFQExtraction,
        quotation: QuotationResult,
    ) -> PriceReviewResult:

        prompt = f"""
    You are an experienced market research pricing reviewer.

    Review the generated quotation.

    RFQ Information
    ---------------
    Project: {rfq.project_name}
    Country: {rfq.country}
    Sample Size: {rfq.sample_size}
    LOI: {rfq.loi}
    IR: {rfq.ir}

    Quotation
    ---------
    Total Cost: {quotation.total_cost}
    Currency: {quotation.currency}

    Determine whether the quotation appears reasonable.

    Return:

    - recommendation: APPROVE, REVIEW or REJECT
    - confidence: number between 0 and 1
    - summary: concise explanation
    """

        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=prompt,
            text_format=PriceReviewResult,
        )

        return response.output_parsed