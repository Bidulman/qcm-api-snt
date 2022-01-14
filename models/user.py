from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    nick: str
    permission: str


class NewUser(BaseModel):
    name: str
    nick: str
    password: str
    permission: str


class EditedUser(BaseModel):
    id: int
    new_name: Optional[str] = None
    new_nick: Optional[str] = None
    new_password: Optional[str] = None
    new_permission: Optional[str] = None


class OldUser(BaseModel):
    id: int
