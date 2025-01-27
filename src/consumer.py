from asyncio import AbstractEventLoop, sleep
from logging import getLogger

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from src.configs import broker_settings
from src.managers import MessagesSpreadingManager, websocket_manager


async def manage_chat_messages(event_loop: AbstractEventLoop) -> None:
    logger = getLogger("manage_chat_messages")
    while True:
        try:
            message_spreading_manager = MessagesSpreadingManager(
                consumer=AIOKafkaConsumer(
                    broker_settings.MESSAGE_TOPIC,
                    bootstrap_servers=broker_settings.BOOTSTRAP_SERVERS,
                    group_id=broker_settings.MESSAGE_TOPIC_GROUP_ID,
                    loop=event_loop,
                ),
                producer=AIOKafkaProducer(
                    bootstrap_servers=broker_settings.BOOTSTRAP_SERVERS,
                    loop=event_loop,
                ),
            )
            async for message in message_spreading_manager.consume_message():
                await websocket_manager.send_message_to_chat(
                    message.chat_id,
                    message.model_dump_json(),
                )
        except Exception as e:
            logger.exception(e)
            await sleep(5)


def start_consuming(loop: AbstractEventLoop):
    loop.create_task(manage_chat_messages(loop))
