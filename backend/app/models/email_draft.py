from pydantic import BaseModel


class DraftEmailResponse(BaseModel):
    subject: str
    body: str