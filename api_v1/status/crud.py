from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.status_names.shemas import StatusNameUpdate
from core.models import Status, StatusName


async def create_status(session: AsyncSession, user_id: int, status_text_id: int, help_user_id: int | None = None) -> Status:
    status = Status(user_id=user_id, status_text_id=status_text_id, help_user_id=help_user_id)
    session.add(status)
    await session.commit()
    return status


async def get_status_names(session: AsyncSession) -> list[StatusName]:
    stmt = select(StatusName).order_by(StatusName.id)
    status_names = await session.scalars(stmt)
    return list(status_names)


async def get_status_name(session: AsyncSession, status_name_id: int) -> StatusName | None:
    stmt = select(StatusName).where(StatusName.id == status_name_id)
    status_name = await session.scalar(stmt)
    return status_name



async def create_status_name(session: AsyncSession, status_name_in) -> StatusName:
    status_name = StatusName(**status_name_in.model_dump())
    session.add(status_name)
    await session.commit()
    return status_name


async def update_status_name(session: AsyncSession, status_name: StatusName, status_name_update: StatusNameUpdate,):
    for name, value in status_name_update.model_dump(exclude_unset=True).items():
        setattr(status_name, name, value)
    await session.commit()
    return status_name


