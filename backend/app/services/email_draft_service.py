from openai import OpenAI
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.email_draft import DraftEmailResponse
from app.prompts.email_draft import EMAIL_DRAFT_SYSTEM_PROMPT
from app.db.repositories.approval_repository import ApprovalRepository
from app.db.repositories.quotation_repository import QuotationRepository
from app.db.repositories.rfq_repository import RFQRepository


class EmailDraftService:

    def __init__(self, db: Session):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

        self.rfq_repository = RFQRepository(db)
        self.quotation_repository = QuotationRepository(db)
        self.approval_repository = ApprovalRepository(db)

    def generate(
        self,
        rfq_id: int,
    ) -> DraftEmailResponse:

        rfq = self.rfq_repository.get_by_id(rfq_id)

        if not rfq:
            raise ValueError("RFQ not found.")

        quotation = self.quotation_repository.get_by_rfq_id(rfq_id)

        if not quotation:
            raise ValueError("This RFQ has not been quoted yet.")

        approval = self.approval_repository.get_by_rfq_id(rfq_id)

        if not approval:
            raise ValueError("This RFQ has not been reviewed yet.")

        if approval.decision.upper() != "APPROVE":
            raise ValueError(
                "An email draft can only be generated for an approved RFQ."
            )

        prompt = f"""
Client Information
------------------
Client Contact: {rfq.client_name}
Client Company: {rfq.client}

RFQ Information
---------------
Project Name: {rfq.project_name}
Country: {rfq.country}
Sample Size: {rfq.sample_size}
Timeline: {rfq.timeline}
Methodology: {rfq.methodology}

Quotation
---------
Total Cost: {quotation.total_cost}
Currency: {quotation.currency}

Sender Information
------------------
Sender Name: {settings.SENDER_NAME}
Company: {settings.COMPANY_NAME}
"""

        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": EMAIL_DRAFT_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            text_format=DraftEmailResponse,
        )

        return response.output_parsed