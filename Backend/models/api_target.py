from pydantic import BaseModel

class APICreate(BaseModel):
    name: str
    url: str


class APIUpdate(BaseModel):
    name: str
    url: str

class APIStatus(BaseModel):
    is_active: bool