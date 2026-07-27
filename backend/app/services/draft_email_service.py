from openai import OpenAI

from app.config.settings import settings
from app.db.repositories.draft_email_repository import DraftEmailRepository
from app.models.draft_email import DraftEmailResult
from app.db.repositories.rfq_repository import RFQRepository
from app.enums.rfq_status import RFQStatus


class DraftEmailService:

    def __init__(self, db):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.repository = DraftEmailRepository(db)
        self.rfq_repository = RFQRepository(db)

    def generate(
        self,
        rfq,
        quotation,
        approval,
    ):
        prompt = f"""
You are an experienced market research sales manager.

Generate a professional quotation email.

Project
-------
{rfq.project_name}

Country
-------
{rfq.country}

Sample Size
-----------
{rfq.sample_size}

Total Price
-----------
{quotation.total_cost} {quotation.currency}

Approval Status
---------------
{approval.decision}

Write a professional email to the client.

Return:

- subject
- body
"""

        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=prompt,
            text_format=DraftEmailResult,
        )

        result = response.output_parsed

        draft = self.repository.create(
            rfq_id=rfq.id,
            quotation_id=quotation.id,
            approval_id=approval.id,
            result=result,
        )

        self.rfq_repository.update_status(
            rfq=rfq,
            status=RFQStatus.EMAIL_DRAFTED,
        )

        return draft