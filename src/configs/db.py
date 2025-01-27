from src.configs.base import DeploySettings


class DBSettings(DeploySettings):
    """
    Class contains data base env params
    """

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @property
    def POSTGRES_URL(self):
        _user = self.POSTGRES_USER
        _password = self.POSTGRES_PASSWORD
        _host = self.POSTGRES_HOST
        _port = self.POSTGRES_PORT
        _db = self.POSTGRES_DB
        url = f"postgresql+asyncpg://{_user}:{_password}@{_host}:{_port}/{_db}"
        return url


db_settings = DBSettings()
