from datetime import datetime

from pydantic import BaseModel


class MessageCreateSchema(BaseModel):
    sender_id: int
    content: str


class MessageRetrieveSchema(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    created_at: datetime
    updated_at: datetime
