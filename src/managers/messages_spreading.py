from json import loads
from typing import AsyncIterator

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from src.configs import broker_settings
from src.schemas import MessageRetrieveSchema


class Singleton(object):
    _instance = None

    def __new__(class_, consumer, producer, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class MessagesSpreadingManager:
    consumer: AIOKafkaConsumer
    producer: AIOKafkaProducer
    _instance = None

    def __new__(cls, consumer, producer, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(MessagesSpreadingManager, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self, consumer, producer, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.consumer = consumer
        self.producer = producer

    async def spread_message(self, message: MessageRetrieveSchema) -> None:
        await self.producer.start()
        try:
            await self.producer.send(
                broker_settings.MESSAGE_TOPIC,
                value=message.model_dump_json().encode(),
            )
        finally:
            ...

    async def consume_message(self) -> AsyncIterator[MessageRetrieveSchema]:
        await self.consumer.start()
        try:
            async for message in self.consumer:
                message_data = loads(message.value)
                yield MessageRetrieveSchema(**message_data)
        finally:
            await self.consumer.stop()


message_spreading_manager = MessagesSpreadingManager(
    None,
    None,
)
