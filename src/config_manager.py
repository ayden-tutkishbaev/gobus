from os.path import join, dirname
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_HOST: str

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_lifetime: int = 30

    model_config = SettingsConfigDict(
        env_file=join(dirname(dirname(__file__)), '.env'),
        env_file_encoding='utf-8'
    )


config = Config()