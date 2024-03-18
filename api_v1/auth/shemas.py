from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserInfo(BaseModel):
    id: int
    email: str
    name: str
    surname: str
