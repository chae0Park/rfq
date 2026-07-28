from sqlalchemy.orm import Session

from app.db.models.approval import ApprovalDB
from app.models.approval import ApprovalRequest


class ApprovalRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        rfq_id: int,
        quotation_id: int,
        request: ApprovalRequest,
    ) -> ApprovalDB:

        approval = ApprovalDB(
            rfq_id=rfq_id,
            quotation_id=quotation_id,
            decision=request.decision,
            reviewer=request.reviewer,
            comment=request.comment,
        )

        self.db.add(approval)
        self.db.commit()
        self.db.refresh(approval)

        return approval

    def get_by_id(
        self,
        approval_id: int,
    ) -> ApprovalDB:

        return (
            self.db.query(ApprovalDB)
            .filter(ApprovalDB.id == approval_id)
            .first()
        )

    def get_by_rfq_id(
        self,
        rfq_id: int,
    ) -> ApprovalDB | None:

        return (
            self.db.query(ApprovalDB)
            .filter(ApprovalDB.rfq_id == rfq_id)
            .order_by(ApprovalDB.created_at.desc())
            .first()
        )