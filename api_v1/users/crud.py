import math

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload

from api_v1.status.schemas import StatusUpdate
from api_v1.users.schemas import UserCreate, UserUpdate
from api_v1.security import generate_otp_code, hash_password, send_email
from core.config import settings
from core.models import Status
from core.models.user import User


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).options(selectinload(User.my_contacts),
                                selectinload(User.for_contacts),
                                joinedload(User.status).joinedload(Status.status_text),
                                selectinload(User.notification_from),
                                selectinload(User.notification_to)).order_by(User.id)
    users = await session.scalars(stmt)
    return list(users)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    code_otp = generate_otp_code()
    user_in.password = hash_password(user_in.password).decode()
    user = User(**user_in.model_dump(), code=code_otp)
    user.status = Status(status_text_id=1)
    session.add(user)
    await session.commit()
    # send_email(subject="Sangel | OTP code", message=f"Your OTP code is {code_otp}", email_receiver=user_in.email)
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).options(selectinload(User.my_contacts),
                                selectinload(User.for_contacts),
                                joinedload(User.status).joinedload(Status.status_text),
                                selectinload(User.notification_from),
                                selectinload(User.notification_to)).where(User.id == user_id)
    user = await session.scalar(stmt)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).options(selectinload(User.my_contacts),
                                selectinload(User.for_contacts),
                                joinedload(User.status).joinedload(Status.status_text),
                                selectinload(User.notification_from),
                                selectinload(User.notification_to)).where(User.email == email)
    user = await session.scalar(stmt)
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def update_user_status(session: AsyncSession, user_id: int, status_update: StatusUpdate):
    status = StatusUpdate(**status_update.dict())
    if status_update.status_text_id is not None:
        stmt = update(Status).where(Status.user_id == user_id).values(status_text_id=status_update.status_text_id, help_user_id=status_update.help_user_id)
    else:
        stmt = update(Status).where(Status.user_id == user_id).values(help_user_id=status_update.help_user_id)
    await session.execute(stmt)
    await session.commit()
    return status


async def get_nearest_users(user_in: User, session: AsyncSession):
    EART_RADIUS = 6371210
    distance = settings.nearest_distance
    deltaLat = math.pi / 180 * EART_RADIUS * math.cos(user_in.latitude * math.pi / 18)
    deltaLon = math.pi / 180 * EART_RADIUS * math.cos(user_in.longitude * math.pi / 18)
    border_left_lat = min(user_in.latitude - distance / deltaLat, user_in.latitude + distance / deltaLon)
    border_right_lat = max(user_in.latitude - distance / deltaLat, user_in.latitude + distance / deltaLon)
    border_left_lon = min(user_in.longitude - distance / deltaLon, user_in.longitude + distance / deltaLon)
    border_right_lon = max(user_in.latitude - distance / deltaLon, user_in.latitude + distance / deltaLon)
    stmt = (select(User).options(selectinload(User.my_contacts),
                                selectinload(User.for_contacts),
                                joinedload(User.status).joinedload(Status.status_text),
                                selectinload(User.notification_from),
                                selectinload(User.notification_to))
            .where(User.latitude.between(border_left_lat, border_right_lat), User.longitude.between(border_left_lon, border_right_lon))
            .order_by(User.id))
    users = await session.scalars(stmt)
    return list(users)


