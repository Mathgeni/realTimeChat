from asyncio import AbstractEventLoop

from fastapi import FastAPI
from sqlalchemy.sql import text
from starlette.middleware.cors import CORSMiddleware
from uvicorn import Config, Server

from src.api import router
from src.configs import app_settings
from src.db.postgres import Session


def get_application() -> FastAPI:
    openapi_tags = [
        {
            "name": "Real Time Chat",
        },
    ]

    application = FastAPI(
        title="Fresh Auto Checkout API microservice",
        debug=app_settings.DEBUG,
        openapi_tags=openapi_tags,
        openapi_url="/real-time-chat/openapi.json",
        redoc_url="/real-time-chat/docs/_r",
        docs_url="/real-time-chat/docs/_s",
    )

    application.include_router(router, prefix="/api")

    @application.get(
        app_settings.HEALTH_ENDPOINT_URL,
        include_in_schema=True,
    )
    async def db_liveness_probe():
        async with Session() as session:
            await session.execute(text("SELECT 1"))
            return {"status": "db is healthy"}

    @application.get(
        app_settings.HEALTH_API_ENDPOINT_URL,
        include_in_schema=True,
    )
    async def api_liveness_probe():
        return {"status": "healthy"}

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


def start_uvicorn(app: FastAPI, loop: AbstractEventLoop):
    config = Config(
        app,
        host=app_settings.API_HOST,
        port=app_settings.API_PORT,
        loop=loop,
        server_header=False,
        workers=1,
    )
    server = Server(config)
    loop.run_until_complete(server.serve())
