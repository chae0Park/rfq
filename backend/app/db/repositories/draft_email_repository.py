from sqlalchemy.orm import Session

from app.db.models.draft_email import DraftEmailDB
from app.models.draft_email import DraftEmailResult


class DraftEmailRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        rfq_id: int,
        quotation_id: int,
        approval_id: int,
        result: DraftEmailResult,
    ) -> DraftEmailDB:

        draft = DraftEmailDB(
            rfq_id=rfq_id,
            quotation_id=quotation_id,
            approval_id=approval_id,
            subject=result.subject,
            body=result.body,
        )

        self.db.add(draft)
        self.db.commit()
        self.db.refresh(draft)

        return draft