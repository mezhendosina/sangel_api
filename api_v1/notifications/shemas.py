from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):
    text: str
    user_to_id: int


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    id: int
    text: str
    is_read: int | None = 0


class Notification(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_from_id: int
    is_read: int

