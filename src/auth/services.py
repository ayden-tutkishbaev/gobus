from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status, Depends, Form
from fastapi.security import (
    HTTPBearer, 
    OAuth2PasswordBearer
)

from src.auth.requests import get_user_by_username
from src.dependencies import db_connection, redis_connection

from src.auth import security

from src.auth.schemas import UserSchema
from src.config import config

from datetime import timedelta


http_bearer = HTTPBearer(auto_error=False)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/users/login',
)


TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


async def validate_auth_user(
    session: db_connection,
    username: str = Form(),
    password: str = Form(),
) -> UserSchema:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={'WWW-Authenticate': 'Basic'}
    )
    user = await get_user_by_username(session, username)
    if not user:
        raise unauthorized_exception
    
    if not security.validate_password(
        password=password,
        hashed_password=user.password_hashed,
    ):
        raise unauthorized_exception

    return user


async def get_current_token_payload(
    redis: redis_connection,
    token: str = Depends(oauth2_scheme)
) -> UserSchema:
    try:
        payload = security.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error {e}"
        )
    jti = payload.get("jti")
    print(jti)
    if jti and await redis.exists(f"blacklist:{jti}"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token has been revoked")
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )
    

async def get_user_by_token_sub(payload: dict, session: db_connection) -> UserSchema:
    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return UserSchema.model_validate(user)
    
    
    # username: str | None = payload.get("sub")
    # if user := users_db.get(username):
    #     return user
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Invalid token"
    # )


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
        session: db_connection,
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload, session)
    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type
        
    async def __call__(self,
                session: db_connection,
                payload: dict = Depends(get_current_token_payload),
            ):
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_sub(payload, session)
    


def create_jwt(
    token_type: str,
    token_data: dict,
    lifetime_min: int = config.access_token_lifetime,
    lifetime_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return security.encode_jwt(
        payload=jwt_payload,
        lifetime_min=lifetime_min,
        lifetime_timedelta=lifetime_timedelta
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }    
    return create_jwt(token_type=ACCESS_TOKEN_TYPE, token_data=jwt_payload,
                      lifetime_min=config.access_token_lifetime)


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    return create_jwt(token_type=REFRESH_TOKEN_TYPE, token_data=jwt_payload, 
                      lifetime_timedelta=timedelta(minutes=config.refresh_token_lifetime),)

