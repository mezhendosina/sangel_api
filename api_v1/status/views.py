from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.security import check_current_token_auth
from api_v1.status import crud
from api_v1.status.dependencies import status_name_by_id
from api_v1.status.schemas import StatusName
from api_v1.status_names.shemas import StatusNameCreate, StatusNameUpdate
from core.models import db_helper

router = APIRouter(tags=['Statuses'])


@router.get("/", response_model=list[StatusName])
async def get_status_names(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                       ):
    return await crud.get_status_names(session=session)


@router.get("/{status_name_id}/", response_model=StatusName)
async def get_status_name(status_name_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                          credentials=Depends(check_current_token_auth)
                       ):
    status_name = await crud.get_status_name(session=session, status_name_id=status_name_id)
    if status_name is not None:
        return status_name
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Status_name {status_name_id} exist!",
    )


@router.post("/", response_model=StatusName, status_code=status.HTTP_201_CREATED)
async def create_status_name(status_name_in: StatusNameCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency),):
    return await crud.create_status_name(session=session, status_name_in=status_name_in)


@router.patch("/{status_name_id}/")
async def update_status(status_name_update: StatusNameUpdate, status_name: StatusName = Depends(status_name_by_id), session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_status_name(session=session, status_name=status_name, status_name_update=status_name_update)
