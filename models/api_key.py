from pydantic import BaseModel


class ApiKey(BaseModel):
    key: str
