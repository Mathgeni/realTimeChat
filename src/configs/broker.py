import uuid

from src.configs.base import DeploySettings


class BrokerSettings(DeploySettings):
    """
    Class contains data base env params
    """

    BROKER_HOST: str
    BROKER_PORT: int

    MESSAGE_TOPIC_GROUP_ID: str = str(uuid.uuid4())
    MESSAGE_TOPIC: str

    @property
    def BOOTSTRAP_SERVERS(self) -> str:
        return f"{self.BROKER_HOST}:{self.BROKER_PORT}"


broker_settings = BrokerSettings()
