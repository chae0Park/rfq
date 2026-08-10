from sqlalchemy.orm import Session

from app.db.repositories.approval_repository import ApprovalRepository
from app.db.repositories.rfq_repository import RFQRepository
from app.models.approval import ApprovalRequest
from app.enums.rfq_status import RFQStatus


class ApprovalService:

    def __init__(self, db: Session):
        self.repository = ApprovalRepository(db)
        self.rfq_repository = RFQRepository(db)

    def approve(
        self,
        rfq,
        quotation_id: int,
        request: ApprovalRequest,
    ):

        approval = self.repository.create(
            rfq_id=rfq.id,
            quotation_id=quotation_id,
            request=request,
        )

        if request.decision == "APPROVE":
            status = RFQStatus.APPROVED

        elif request.decision == "REJECT":
            status = RFQStatus.REJECTED

        self.rfq_repository.update_status(
            rfq=rfq,
            status=status,
        )

        return approval