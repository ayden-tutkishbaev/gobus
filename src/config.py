from os.path import join, dirname, abspath
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_HOST: str
    
    SUPER_ADMIN_USERNAME: str
    SUPER_ADMIN_PASSWORD: str
    SUPER_ADMIN_PHONE_NUMBER: str

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_lifetime: int = 30
    
    max_upload_size_bytes: int = 5 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=join(dirname(dirname(abspath(__file__))), '.env'),
        env_file_encoding='utf-8'
    )


config = Config()