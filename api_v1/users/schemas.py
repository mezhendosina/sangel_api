from pydantic import BaseModel, ConfigDict

from api_v1.contacts.shemas import Contact
from api_v1.notifications.shemas import Notification
from api_v1.status.schemas import Status


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    name: str
    surname: str


class UserAuth(UserBase):
    pass


class UserCodeValidate(BaseModel):
    id: int
    code: str


class UserUpdate(UserCreate):
    email: str | None = None
    password: str | None = None
    name: str | None = None
    surname: str | None = None
    image: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    access: int | None = None
    device_id: str | None = None
    code: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    access: int
    longitude: float | None = None
    latitude: float | None = None
    code: str | None
    image: str | None = None
    my_contacts: list[Contact] | None
    for_contacts: list[Contact] | None
    status: Status | None
    notification_to: list[Notification] | None
    notification_from: list[Notification] | None


