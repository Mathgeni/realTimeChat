from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.exc import IntegrityError

from src.db.postgres import get_postgres_repository
from src.db.postgres.models import Chats, Participants
from src.db.postgres.repos import ChatsRepository, ParticipantsRepository
from src.managers import websocket_manager
from src.responses import (
    chat_create_participants,
    chat_create_responses,
    chat_list_responses,
    chat_retrieve_responses,
)
from src.schemas import (
    ChatCreateSchema,
    ChatListSchema,
    ChatRetrieveSchema,
    ParticipantAddSchema,
)


router = APIRouter()


@router.post(
    "/create",
    responses=chat_create_responses,
    status_code=201,
)
async def create_chat(
    chat_create_schema: ChatCreateSchema,
    chats_repository: ChatsRepository = Depends(
        get_postgres_repository(ChatsRepository)
    ),
    participants_repository: ParticipantsRepository = Depends(
        get_postgres_repository(ParticipantsRepository)
    ),
) -> Response:
    try:
        chat_model = Chats(
            name=chat_create_schema.name,
            creator_id=chat_create_schema.creator.user_id,
        )
        chat_id = await chats_repository.create(chat_model)
        participant = Participants(
            name=chat_create_schema.creator.name,
            user_id=chat_create_schema.creator.user_id,
            chat_id=chat_id,
        )
        await participants_repository.create(participant)
        return Response(
            status_code=201,
        )
    except IntegrityError:
        status_code = 409
        raise HTTPException(
            status_code=status_code,
            detail=chat_create_responses.get_user_connection_map(status_code),
        )
    finally:
        await chats_repository.session.close()
        await participants_repository.session.close()


@router.get(
    "/{chat_id}",
    response_model=ChatRetrieveSchema,
    responses=chat_retrieve_responses,
)
async def retrieve_chat(
    chat_id: int,
    chats_repository: ChatsRepository = Depends(
        get_postgres_repository(ChatsRepository)
    ),
) -> ChatRetrieveSchema:
    chat_model = await chats_repository.get_by_id(chat_id)
    if chat_model is None:
        await chats_repository.session.close()
        raise HTTPException(
            status_code=404,
            detail=chat_retrieve_responses.get_user_connection_map(404),
        )
    data = chat_model.dict()
    for participant in chat_model.participants:
        data["participants"] = data.get("participants", []) + [
            participant.dict()
        ]
    return ChatRetrieveSchema(**data)


@router.get(
    "",
    response_model=list[ChatListSchema],
    responses=chat_list_responses,
)
async def retrieve_chat_list(
    creator_id: int,
    limit: int = 20,
    offset: int = 0,
    chats_repository: ChatsRepository = Depends(
        get_postgres_repository(ChatsRepository)
    ),
) -> list[ChatListSchema]:
    chat_models = await chats_repository.list_by_creator_id(
        creator_id,
        limit,
        offset,
    )
    return [ChatListSchema(**x.dict()) for x in chat_models]


@router.post(
    "/add/participant",
    responses=chat_create_participants,
    status_code=201,
)
async def add_chat_participant(
    participant_add_schema: ParticipantAddSchema,
    participants_repository: ParticipantsRepository = Depends(
        get_postgres_repository(ParticipantsRepository)
    ),
) -> Response:
    try:
        participant = Participants(
            name=participant_add_schema.name,
            user_id=participant_add_schema.user_id,
            chat_id=participant_add_schema.chat_id,
        )
        await participants_repository.create(participant)
        return Response(
            status_code=201,
        )
    except IntegrityError:
        status_code = 409
        raise HTTPException(
            status_code=status_code,
            detail=chat_create_participants.get_user_connection_map(
                status_code
            ),
        )
    finally:
        await participants_repository.session.close()


@router.websocket("/ws/{chat_id}/{user_id}")
async def websocket_chat(
    chat_id: int,
    user_id: int,
    websocket: WebSocket,
):
    try:
        await websocket_manager.handle_connection(chat_id, user_id, websocket)
    except WebSocketDisconnect:
        await websocket_manager.delete_connection(chat_id, user_id)
