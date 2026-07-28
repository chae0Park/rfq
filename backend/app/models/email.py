from pydantic import BaseModel


class EmailRequest(BaseModel):
    from_name: str | None = None
    from_email: str | None = None
    subject: str
    body: str