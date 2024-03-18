from fastapi import HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated

from api_v1.notifications import crud
from core.models import db_helper, Notification


async def notification_by_id(notification_id: Annotated[int, Path], session: AsyncSession = Depends(db_helper.scoped_session_dependency),) -> Notification:
    notification = await crud.get_notification(session=session, notification_id=notification_id)
    if notification is not None:
        return notification

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Notification {notification_id} not found!",
    )
