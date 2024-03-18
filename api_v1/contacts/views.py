from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.contacts import crud
from api_v1.contacts.dependencies import contact_by_id
from api_v1.contacts.shemas import Contact, ContactCreate
from api_v1.security import check_current_token_auth
from api_v1.users.crud import get_user
from core.models.db_helper import db_helper

router = APIRouter(tags=['Contacts'])


@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(contact_in: ContactCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)):
    user_id = credentials.get("sub")
    user = await get_user(session, user_id)
    if user is not None:
        return await crud.create_contact(session=session, contact_in=contact_in, user_id=user_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )


@router.delete("/{contact_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact: Contact = Depends(contact_by_id), session: AsyncSession = Depends(db_helper.scoped_session_dependency), credentials=Depends(check_current_token_auth)) -> None:
     await crud.delete_contact(session=session, contact=contact)


