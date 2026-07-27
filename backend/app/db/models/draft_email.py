from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.sql import func

from app.config.database import Base


class DraftEmailDB(Base):
    __tablename__ = "draft_emails"

    id = Column(Integer, primary_key=True, index=True)

    rfq_id = Column(
        Integer,
        ForeignKey("rfqs.id"),
        nullable=False,
    )

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=False,
    )

    approval_id = Column(
        Integer,
        ForeignKey("approvals.id"),
        nullable=False,
    )

    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )