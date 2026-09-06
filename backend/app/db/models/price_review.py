from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class PriceReviewDB(Base):
    __tablename__ = "price_reviews"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    rfq_id: Mapped[int] = mapped_column(
        ForeignKey("rfqs.id"),
        nullable=False,
        index=True,
    )

    quotation_id: Mapped[int] = mapped_column(
        ForeignKey("quotations.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    benchmark_low: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    benchmark_high: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    source_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )