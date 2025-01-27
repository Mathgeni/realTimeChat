from fastapi import APIRouter

from .chats import router as chats_router
from .messages import router as messages_router


router = APIRouter()

router.include_router(chats_router, prefix="/chats", tags=["Chats"])
router.include_router(messages_router, prefix="/chats", tags=["Messages"])
