from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.email_draft import DraftEmailResponse

from app.db.repositories.approval_repository import ApprovalRepository
from app.db.repositories.quotation_repository import QuotationRepository
from app.db.repositories.rfq_repository import RFQRepository



class EmailDraftService:

    def __init__(self, db: Session):
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

        subject = (
            f"Quotation - {rfq.project_name}"
            if rfq.project_name
            else "Quotation for Your RFQ"
        )

        body = f"""Hi {rfq.client_name},

Thank you for your RFQ.

Based on the project requirements provided, we are pleased to offer
a quotation for the following study:

Country: {rfq.country}
Sample Size: {rfq.sample_size}
Methodology: {rfq.methodology}

Total Quotation: {quotation.currency} {quotation.total_cost:,.2f}

Please let us know if you have any questions.

Best regards,
{settings.SENDER_NAME}
{settings.COMPANY_NAME}
        """

        return DraftEmailResponse(
            subject=subject,
            body=body,
        )