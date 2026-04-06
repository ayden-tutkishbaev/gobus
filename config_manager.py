from os.path import join, dirname
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
                
    model_config = SettingsConfigDict(
        env_file=join(dirname(__file__), '.env'),
        env_file_encoding='utf-8'
    )
    

config = Config()