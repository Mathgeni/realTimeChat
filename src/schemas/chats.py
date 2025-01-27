from datetime import datetime

from pydantic import BaseModel


class Participant(BaseModel):
    user_id: int
    name: str


class ParticipantAddSchema(BaseModel):
    chat_id: int
    participant: Participant


class ChatCreateSchema(BaseModel):
    name: str
    creator: Participant


class ChatRetrieveSchema(BaseModel):
    id: int
    name: str
    creator_id: int
    created_at: datetime
    participants: list[Participant]


class ChatListSchema(BaseModel):
    id: int
    name: str
