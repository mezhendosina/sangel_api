from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.notifications.shemas import NotificationUpdate
from core.models.notification import Notification


async def create_notification(session: AsyncSession, notification_in, user_id) -> Notification:
    notification = Notification(**notification_in.model_dump(), user_from_id=user_id)
    session.add(notification)
    await session.commit()
    return notification


async def get_notification(session: AsyncSession, notification_id: int) -> Notification | None:
    stmt = select(Notification).where(Notification.id == notification_id)
    user = await session.scalar(stmt)
    return user


async def update_notification(
    session: AsyncSession,
    notification: Notification,
    notification_update: NotificationUpdate,
) -> Notification:
    for name, value in notification_update.model_dump(exclude_unset=True).items():
        setattr(notification, name, value)
    await session.commit()
    return notification


async def delete_notification(session: AsyncSession, notification: Notification) -> None:
    await session.delete(notification)
    await session.commit()
