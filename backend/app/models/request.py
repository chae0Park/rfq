from pydantic import BaseModel, Field


class RFQRequest(BaseModel):
    from_name: str | None = None
    from_email: str | None = None
    subject: str | None = None
    email_body: str
    thread_id: str | None = None
    message_id: str | None = None