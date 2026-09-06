from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.config.database import Base
from sqlalchemy import Enum
from app.enums.rfq_status import RFQStatus


class RFQDB(Base):
    __tablename__ = "rfqs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    original_email: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    gmail_thread_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    gmail_message_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    project_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    client: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    client_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    client_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    countries: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    region: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    target_audience: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    gender: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    age: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    quota: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sample_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    loi: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    ir: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    methodology: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    timeline: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    languages: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    
    project_scope: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    end_client: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    additional_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    programming_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    translation_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    overlay_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    rush: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    client_tier: Mapped[str] = mapped_column(
        String(50),
        default="Standard",
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="USD",
        nullable=False,
    )

    missing_fields: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    clarification_questions: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    ready_for_quotation: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    n8n_resume_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[RFQStatus] = mapped_column(
        Enum(RFQStatus),
        default=RFQStatus.RECEIVED,
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

    