from pydantic import BaseModel


class ApiInfo(BaseModel):
    host: str
    port: int
