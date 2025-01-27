from asyncio import sleep
from logging import getLogger

from fastapi import WebSocket, WebSocketDisconnect


class ChatWebSocketsContainer:
    def __init__(self) -> None:
        self.container: dict[int, dict[int, WebSocket]] = dict()

    def add(
        self,
        chat_id: int,
        user_id: int,
        connection: WebSocket,
    ) -> None:
        self.container.setdefault(chat_id, {}).update({user_id: connection})

    def get_user_connection_map(
        self,
        chat_id: int,
    ) -> dict[int, WebSocket] | None:
        return self.container.get(chat_id)

    def get_user_connection(
        self,
        chat_id: int,
        user_id: int,
    ) -> WebSocket | None:
        return self.container.get(chat_id, {}).get(user_id)

    def delete(
        self,
        chat_id: int,
        user_id: int,
    ) -> WebSocket | None:
        if chat_id in self.container and user_id in self.container[chat_id]:
            websocket = self.container[chat_id].pop(user_id, None)
            if not self.container[chat_id]:
                self.container.pop(chat_id, None)
            return websocket


class WebSocketManager:
    def __init__(self) -> None:
        self._connections: ChatWebSocketsContainer = ChatWebSocketsContainer()
        self._logger = getLogger("WebSocketManager")

    async def handle_connection(
        self,
        chat_id: int,
        user_id: int,
        connection: WebSocket,
    ) -> None:
        await connection.accept()
        self._connections.add(chat_id, user_id, connection)
        while True:
            data = await connection.receive()
            if data.get("type") == "websocket.disconnect":
                await self.delete_connection(chat_id, user_id)
                break
            await sleep(5)

    async def delete_connection(self, chat_id: int, user_id: int) -> None:
        self._connections.delete(chat_id, user_id)

    async def send_message_to_chat(self, chat_id: int, message: str) -> None:
        connections = self._connections.get_user_connection_map(chat_id)
        if connections:
            closed_connections_during_runtime = (
                await self.send_message_to_websocket(connections, message)
            )
            for user_id in closed_connections_during_runtime:
                await self.delete_connection(chat_id, user_id)

    async def send_message_to_websocket(
        self,
        connections: dict[int, WebSocket],
        message: str,
    ) -> set[int]:
        disconnected_users = set()
        for user_id, connection in connections.items():
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected_users.add(user_id)
            except Exception:
                self._logger.exception("Could not send message")

        return disconnected_users


websocket_manager = WebSocketManager()
