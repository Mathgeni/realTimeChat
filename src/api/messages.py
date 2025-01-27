from fastapi import APIRouter, Depends, Response

from src.db.postgres import get_postgres_repository
from src.db.postgres.models import Messages
from src.db.postgres.repos import MessagesRepository
from src.managers import message_spreading_manager
from src.schemas import MessageCreateSchema, MessageRetrieveSchema


router = APIRouter()


@router.post(
    "/{chat_id}/messages",
    status_code=201,
)
async def create_message(
    chat_id: int,
    message_create_schema: MessageCreateSchema,
    messages_repository: MessagesRepository = Depends(
        get_postgres_repository(MessagesRepository)
    ),
) -> Response:
    message_model = Messages(
        chat_id=chat_id,
        sender_id=message_create_schema.sender_id,
        content=message_create_schema.content,
    )
    message_db = await messages_repository.create(message_model)
    message_schema = MessageRetrieveSchema(**message_db.dict())
    await message_spreading_manager.spread_message(message_schema)
    return Response(status_code=201)


@router.get("/{chat_id}/messages")
async def retrieve_messages(
    chat_id: int,
    limit: int = 20,
    offset: int = 0,
    messages_repository: MessagesRepository = Depends(
        get_postgres_repository(MessagesRepository)
    ),
) -> list[MessageRetrieveSchema]:
    messages = await messages_repository.list_messages(chat_id, limit, offset)
    return [MessageRetrieveSchema(**x.dict()) for x in messages]
