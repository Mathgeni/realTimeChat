from os import environ

from pydantic_settings import BaseSettings, SettingsConfigDict


STAGE = environ.get("STAGE", "DEV")


class DeploySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"deploy/{STAGE.lower()}/.env",
        extra="ignore",
    )


deploy_settings = DeploySettings()
