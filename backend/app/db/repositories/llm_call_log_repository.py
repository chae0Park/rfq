from sqlalchemy.orm import Session

from app.db.models.llm_call_log import LLMCallLogDB


class LLMCallLogRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        rfq_id: int | None,
        task_type: str,
        model: str,
        status: str,
        latency_ms: float | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        estimated_cost: float | None = None,
        error_message: str | None = None,
    ) -> LLMCallLogDB:

        log = LLMCallLogDB(
            rfq_id=rfq_id,
            task_type=task_type,
            model=model,
            status=status,
            latency_ms=latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=estimated_cost,
            error_message=error_message,
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log
    
    def get_by_rfq_id(
        self,
        rfq_id: int,
    ) -> list[LLMCallLogDB]:

        return (
            self.db.query(LLMCallLogDB)
            .filter(LLMCallLogDB.rfq_id == rfq_id)
            .order_by(LLMCallLogDB.created_at.asc())
            .all()
        )

    def get_all(
        self,
    ) -> list[LLMCallLogDB]:

        return (
            self.db.query(LLMCallLogDB)
            .order_by(LLMCallLogDB.created_at.desc())
            .all()
        )
    