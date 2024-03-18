from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.status import crud
from core.models import User, StatusName
from core.models import db_helper


async def status_name_by_id(status_name_id: Annotated[int, Path], session: AsyncSession = Depends(db_helper.scoped_session_dependency),) -> StatusName:
    status_name = await crud.get_status_name(session=session, status_name_id=status_name_id)
    if status_name is not None:
        return status_name

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"StatusName {status_name} not found!",
    )

