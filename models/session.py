from pydantic import BaseModel


class Session(BaseModel):
    token: str


class NewSession(BaseModel):
    username: str
    password: str
