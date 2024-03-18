from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.notifications import crud
from api_v1.notifications.dependencies import notification_by_id
from api_v1.notifications.shemas import Notification, NotificationCreate, NotificationUpdate
from api_v1.security import check_current_token_auth
from api_v1.users.crud import get_user
from core.models import db_helper

router = APIRouter(tags=['Notifications'])


@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification(notification_in: NotificationCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)):
    user_id = credentials.get("sub")
    user = await get_user(session, user_id)
    if user is not None:
        return await crud.create_notification(session=session, notification_in=notification_in, user_id=user_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )


@router.patch("/update/")
async def notification_user(notification_update: NotificationUpdate,  session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)):
    notification = await crud.get_notification(session=session, notification_id=notification_update.id)
    if notification is not None:
        return await crud.update_notification(session=session, notification=notification, notification_update=notification_update)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Notification {notification_update.id} not found!",
    )


@router.delete("/{notification _id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(notification: Notification = Depends(notification_by_id), session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)) -> None:
     await crud.delete_notification(session=session, notification=notification)