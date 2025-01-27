from src.configs.base import DeploySettings


class AppSettings(DeploySettings):
    """
    Class contains data base env params
    """

    DEBUG: bool = False
    HEALTH_ENDPOINT_URL: str = "/health-db"
    HEALTH_API_ENDPOINT_URL: str = "/health-api"

    API_HOST: str = "localhost"
    API_PORT: int = 8000


app_settings = AppSettings()
