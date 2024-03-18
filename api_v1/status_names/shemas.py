from pydantic import BaseModel, ConfigDict


class StatusNameBase(BaseModel):
    text: str


class StatusNameCreate(StatusNameBase):
    pass


class StatusNameUpdate(StatusNameCreate):
    text: str


class StatusName(StatusNameBase):
    model_config = ConfigDict(from_attributes=True)

    id: int