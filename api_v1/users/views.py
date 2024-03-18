import os
import shutil
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.notifications.crud import create_notification
from api_v1.notifications.shemas import NotificationCreate
from api_v1.security import check_current_token_auth
from api_v1.status.schemas import StatusUpdate, Status
from api_v1.users import crud
from api_v1.users.dependencies import user_by_id
from api_v1.users.schemas import UserCreate, User, UserUpdate
from core.config import settings
from core.models import Notification
from core.models.db_helper import db_helper

from fastapi.responses import FileResponse


router = APIRouter(tags=['Users'])


@router.get("/", response_model=list[User])
async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        credentials=Depends(check_current_token_auth)
                       ):
    return await crud.get_users(session=session)


@router.get("/my/", response_model=User)
async def get_user(session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)):
    return await crud.get_user(session=session, user_id=credentials.get("sub"))


@router.get("/{user_id}/", response_model=User)
async def get_user_by_id(user: User = Depends(user_by_id), credentials=Depends(check_current_token_auth)):
    return user


@router.patch("/update/")
async def update_user(user_update: UserUpdate,  session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)):
    user = await crud.get_user(session=session, user_id=credentials.get("sub"))
    return await crud.update_user(session=session, user=user, user_update=user_update)


@router.patch("/user_status/")
async def update_user_status(status_update: StatusUpdate, session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)):
    user = await crud.get_user(session=session, user_id=credentials.get("sub"))
    if user.status.status_text_id == 1 and status_update.status_text_id == 2:
        await send_notifications(user, session, 1)
    elif user.status.status_text_id == 2 and status_update.status_text_id == 1:
        await send_notifications(user, session, 2)
    elif user.status.status_text_id == 1 and status_update.status_text_id == 3 and status_update.help_user_id is not None:
        await send_notifications(user, session, 3, status_update.help_user_id)
    return await crud.update_user_status(session=session, user_id=credentials.get("sub"), status_update=status_update)


@router.post("/nearest/", response_model=list[User])
async def get_nearest_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)):
    user = await crud.get_user(session=session, user_id=credentials.get("sub"))
    if user.latitude is not None and user.longitude is not None:
        return await crud.get_nearest_users(user_in=user, session=session)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"The user don't have information about latitude and longitude"
    )


async def send_notifications(user: User, session: AsyncSession, alert_type: int, help_user_id: int = None):
    if alert_type == 1:
        for contact in user.my_contacts:
            notification_in = NotificationCreate(text="Я нахожусь в опасноти. Мне срочно нужна помощь", user_to_id=contact.contact_user_id)
            await create_notification(session=session, notification_in=notification_in, user_id=user.id)
        nearest_users = []
        if user.latitude is not None and user.longitude is not None:
            nearest_users = await crud.get_nearest_users(user_in=user, session=session)
        for nearest_user in nearest_users:
            notification_in = NotificationCreate(text="Я нахожусь в опасноти. Мне срочно нужна помощь",
                                                 user_to_id=nearest_user.id)
            await create_notification(session=session, notification_in=notification_in, user_id=user.id)
    elif alert_type == 2:
        for contact in user.my_contacts:
            notification_in = NotificationCreate(text="Со мной все хорошо", user_to_id=contact.contact_user_id)
            await create_notification(session=session, notification_in=notification_in, user_id=user.id)
    elif alert_type == 3:
        notification_in = NotificationCreate(text="Спешу к вам на помощь", user_to_id=help_user_id)
        await create_notification(session=session, notification_in=notification_in, user_id=user.id)


@router.post("/upload/", response_model=User)
async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)):
    file.file.seek(0, 2)
    file_size = file.file.tell()
    await file.seek(0)
    if file_size > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()
    with open(f"{settings.image_directory}/{file.filename}", "wb") as f:
        f.write(contents)
    user = await crud.get_user(session=session, user_id=credentials.get("sub"))
    return await crud.update_user(session=session, user=user, user_update=UserUpdate(image=file.filename))


@router.get("/user_image/")
async def show_user_image(filename: str, credentials=Depends(check_current_token_auth)):
    return FileResponse(f"{settings.image_directory}/{filename}", media_type="image/png")