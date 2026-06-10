from fastapi import APIRouter, Form, HTTPException, status, Depends
from sqlalchemy import select

from src.auth.schemas import TokenInfo, UserSchema
from src.auth.models import User
from src.config import config

from src.dependencies import db_connection, redis_connection

from sqlalchemy.orm import selectinload

from time import time

from src.auth.services import (
    ACCESS_TOKEN_TYPE, 
    REFRESH_TOKEN_TYPE, 
    UserGetterFromToken, 
    create_refresh_token, 
    create_access_token,
    get_auth_user_from_token_of_type, 
    get_current_token_payload, 
    http_bearer, validate_auth_user
)

from src.auth.sms_codes import generate_otp, otp_key, lock_key, resend_key


user = APIRouter(
    dependencies=[Depends(http_bearer)],
    prefix="/auth",
    tags=['Auth']
)


@user.post("/login/request-sms")
async def auth_user_login_and_request_sms_code(
    redis: redis_connection,
    user: UserSchema = Depends(validate_auth_user),
):
    user_phone_number = user.phone_number

    if await redis.exists(resend_key(user_phone_number)):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
                            detail="Wait before requesting a new code")

    attempts = await redis.get(lock_key(user_phone_number))
    if attempts and int(attempts) >= config.attempts:
        ttl = await redis.ttl(lock_key(user_phone_number))
        minutes, seconds = divmod(ttl, 60)
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail=f"Too many attempts. Try again in {minutes}m {seconds}s")

    code = generate_otp()
    await redis.set(otp_key(user_phone_number), code, ex=config.sms_code_lifetime)
    
    await redis.set(resend_key(user_phone_number), 1, ex=config.sms_resend_period)

    # send_sms(user_phone_number, code) - TBD
    
    return {"detail": "SMS code has been sent"}

    
@user.post("/login/verify-sms", response_model=TokenInfo)
async def verify_sms_code_and_issue_jwt(
    db: db_connection,
    redis: redis_connection,
    user_phone_number: str = Form(),
    user_code: str = Form(),
):
    
    expected_code = await redis.get(otp_key(user_phone_number))
    print(f"EXPECTED {expected_code}, GIVEN {user_code}")
    
    if not expected_code or expected_code != user_code:
        pipe = redis.pipeline()
        pipe.incr(lock_key(user_phone_number))
        pipe.expire(lock_key(user_phone_number), config.sms_lock_period, xx=True)  
        results = await pipe.execute()

        new_attempts = results[0]
        if new_attempts == 1:
            await redis.expire(lock_key(user_phone_number), config.sms_lock_period) 

        if new_attempts > config.attempts:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
                                detail="Too many attempts. Try again later")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired code")
        
    result = await db.execute(
        select(User)
        .options(selectinload(User.staff))
        .where(User.phone_number == user_phone_number)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")
    
    await redis.delete(otp_key(user_phone_number), lock_key(user_phone_number))
    
    return TokenInfo(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
    )   
    
    
@user.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True,)
async def auth_refresh_jwt(
    user: UserSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE))
):
    access_token = create_access_token(user)
    
    return TokenInfo(
        access_token=access_token,
    )


@user.post("/logout")
async def logout(
    redis: redis_connection,
    payload: dict = Depends(get_current_token_payload),
):
    jti = payload.get("jti")
    exp = payload.get("exp")
    
    if jti and exp:
        ttl = int(exp - time())  
        if ttl > 0:
            await redis.set(f"blacklist:{jti}", 1, ex=ttl)
    
    return {"detail": "Logged out successfully"}

    
@user.get(path="/users/me", response_model=UserSchema)
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)),
):
    return user.model_copy(update={"logged_in_at": payload.get("iat")})