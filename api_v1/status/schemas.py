from pydantic import BaseModel, ConfigDict

from api_v1.status_names.shemas import StatusName


class StatusBase(BaseModel):
    user_id: int
    status_text_id: int
    help_user_id: int | None


class StatusCreate(StatusBase):
    pass


class StatusUpdate(BaseModel):
    status_text_id: int| None = None
    help_user_id: int | None = None


class Status(StatusBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status_text: StatusName | None


