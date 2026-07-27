from pydantic import BaseModel


class DraftEmailResult(BaseModel):
    subject: str
    body: str