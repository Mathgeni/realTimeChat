import asyncio

from src.app import get_application, start_uvicorn
from src.consumer import start_consuming


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_consuming(loop)
    app = get_application()
    start_uvicorn(app, loop)
