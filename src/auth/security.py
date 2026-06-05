from datetime import datetime, timedelta
import uuid

import jwt
import bcrypt
from src.config import config
from src.database.tools import tashkent_now


def encode_jwt(
    payload: dict,
    private_key: str = config.private_key_path.read_text(),
    algorithm: str = config.algorithm,
    lifetime_min: int = config.access_token_lifetime,
    lifetime_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = tashkent_now()
    
    if lifetime_timedelta:
        lifetime = now + lifetime_timedelta
    else:
        lifetime = now + timedelta(minutes=lifetime_min)
    
    to_encode.update(
        exp=lifetime,
        iat=now,
        jti=str(uuid.uuid4())
    )
    encoded = jwt.encode(
        to_encode, 
        private_key, 
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = config.public_key_path.read_text(),
    algorithm: str = config.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm],)
    return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)
    

def validate_password(
    password: str,
    hashed_password: bytes    
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
    
    
