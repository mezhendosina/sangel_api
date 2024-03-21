from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from api_v1.auth.shemas import TokenInfo, UserInfo
from api_v1.auth.utils import encode_jwt
from api_v1.security import validate_password, check_email, generate_otp_code, send_email
from api_v1.users import crud
from api_v1.users.crud import get_user, get_user_by_email
from api_v1.users.schemas import UserCreate, UserUpdate, UserAuth, UserCodeValidate
from core.models import db_helper


router = APIRouter(tags=['Auth'])


@router.post("/login/", response_model=UserInfo)
async def login_user(user_in: UserCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await get_user_by_email(session, user_in.email)
    if user is None:
        if check_email(user_in.email):
            user = await crud.create_user(session=session, user_in=user_in)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid email",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_in.email}' already exist!",
        )
    return UserInfo(id=user.id, email=user.code, name=user.name, surname=user.surname)


@router.post("/login_debug/", response_model=UserInfo)
async def login_user(user_in: UserCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await get_user_by_email(session, user_in.email)
    if user is None:
        if check_email(user_in.email):
            pass
            # user = await crud.create_user(session=session, user_in=user_in)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid email",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_in.email}' already exist!",
        )
    return UserInfo(id=0, email=user_in.email, name=user_in.name, surname=user_in.surname)


@router.post("/", response_model=TokenInfo)
async def auth_user(user_auth: UserAuth, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await get_user_by_email(session, user_auth.email)
    if user is None or not validate_password(
            password=user_auth.password,
            hashed_password=user.password.encode(),
    ) :
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    if user.access == 1:
        jwt_payload = {
            "sub": user.id,
            "email": user.email
        }
        access_token = encode_jwt(jwt_payload)
        return TokenInfo(access_token=access_token, token_type="Bearer")
    new_code_otp = generate_otp_code()
    await crud.update_user(session=session, user=user, user_update=UserUpdate(code=new_code_otp))
    #send_email(subject="Sangel | OTP code", message=f"Your OTP code is {new_code_otp}", email_receiver=user.email)
    return JSONResponse(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content={"id": user.id, "detail": f"User is inactive, The code has just been sent, check email {user.email}"})


@router.post("/validate/", response_model=TokenInfo)
async def validate_user(user_auth: UserCodeValidate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await get_user(session, user_auth.id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_auth.id} not found!",
        )
    if user.code != user_auth.code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid code",
        )
    await crud.update_user(session=session, user=user, user_update=UserUpdate(access=1))
    jwt_payload = {
        "sub": user.id,
        "email": user.email
    }
    access_token = encode_jwt(jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer")
