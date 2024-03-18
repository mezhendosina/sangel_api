from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Contact


async def create_contact(session: AsyncSession, contact_in, user_id) -> Contact:
    contact = Contact(**contact_in.model_dump(), user_id=user_id)
    session.add(contact)
    await session.commit()
    return contact


async def get_contact(session: AsyncSession, contact_id: int) -> Contact | None:
    stmt = select(Contact).where(Contact.id == contact_id)
    contact = await session.scalar(stmt)
    return contact


async def delete_contact(session: AsyncSession, contact: Contact) -> None:
    await session.delete(contact)
    await session.commit()
