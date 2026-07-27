from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.config.database import Base


class QuotationDB(Base):
    __tablename__ = "quotations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    rfq_id: Mapped[int] = mapped_column(
        ForeignKey("rfqs.id"),
        nullable=False,
    )

    base_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    sample_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    programming_fee: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    translation_fee: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    pm_fee: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    margin: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    rush_fee: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    client_discount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    total_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )