from pydantic import BaseModel, ConfigDict


class ContactBase(BaseModel):
    contact_user_id: int


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
