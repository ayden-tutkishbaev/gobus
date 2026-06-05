from os.path import join, dirname, abspath
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_HOST: str
    
    SUPERADMIN_USERNAME: str
    SUPERADMIN_PASSWORD: str
    SUPERADMIN_PHONE_NUMBER: str
    
    REDIS_HOST: str
    REDIS_PORT: int
        
    
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_lifetime: int = 15
    refresh_token_lifetime: int = 60 * 24 * 30
    
    sms_code_lifetime: int = 300
    sms_resend_period: int = 60
    sms_lock_period: int = 600
    attempts: int = 5
    
    max_upload_size_bytes: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=join(dirname(dirname(abspath(__file__))), '.env'),
        env_file_encoding='utf-8'
    )


config = Config()