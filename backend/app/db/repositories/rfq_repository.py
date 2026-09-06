from sqlalchemy.orm import Session

from app.db.mappers.rfq_mapper import RFQMapper
from app.db.models.rfq import RFQDB
from app.enums.rfq_status import RFQStatus
from app.models.result import RFQExtractionResult
from app.models.request import RFQRequest


class RFQRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        request: RFQRequest,
        result: RFQExtractionResult,
    ):

        rfq_db = RFQMapper.to_db(
            request=request,
            result=result,
        )

        self.db.add(rfq_db)
        self.db.commit()
        self.db.refresh(rfq_db)

        return rfq_db
    

    def update_status(
        self,
        rfq: RFQDB,
        status: RFQStatus,
    ) -> RFQDB:

        rfq.status = status

        self.db.commit()
        self.db.refresh(rfq)

        return rfq

    def update_to_quoted(
        self,
        rfq,
    ):
        rfq.status = RFQStatus.QUOTED

        self.db.commit()
        self.db.refresh(rfq)

        return rfq

    def get_all(self):
        return (
            self.db.query(RFQDB)
            .order_by(RFQDB.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        rfq_id: int,
    ):
        return (
            self.db.query(RFQDB)
            .filter(RFQDB.id == rfq_id)
            .first()
        )

    def get_by_thread_id(
        self,
        thread_id: str,
    ):
        return (
            self.db.query(RFQDB)
            .filter(RFQDB.gmail_thread_id == thread_id)
            .order_by(RFQDB.created_at.desc())
            .first()
        )

    def update(
        self,
        rfq,
        update_data: dict,
    ):
        for field, value in update_data.items():
            setattr(rfq, field, value)

        self.db.commit()
        self.db.refresh(rfq)

        return rfq



