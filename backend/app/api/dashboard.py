from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.db.repositories.rfq_repository import RFQRepository

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/rfqs")
def get_rfqs(
    db: Session = Depends(get_db),
):
    repository = RFQRepository(db)
    return repository.get_all()


@router.get("/rfqs/{rfq_id}")
def get_rfq(
    rfq_id: int,
    db: Session = Depends(get_db),
):
    repository = RFQRepository(db)

    rfq = repository.get_by_id(rfq_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found.",
        )

    return rfq