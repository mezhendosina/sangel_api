from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.contacts import crud
from core.models import db_helper, Contact


async def contact_by_id(contact_id: Annotated[int, Path], session: AsyncSession = Depends(db_helper.scoped_session_dependency),) -> Contact:
    contact = await crud.get_contact(session=session, contact_id=contact_id)
    if contact is not None:
        return contact

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Contact {contact_id} not found!",
    )

