# api_target.py - This file defines the Pydantic models for the API targets that we want to monitor. These models include APICreate for creating new API targets, APIUpdate for updating existing API targets, and APIStatus for updating the active status of an API target. Each model defines the necessary fields and their types, which will be used for data validation when handling requests in the API routes. By using Pydantic models, we can ensure that the data we receive in our API endpoints is structured correctly and meets the expected format before processing it further.

from pydantic import BaseModel

class APICreate(BaseModel):
    name: str
    url: str


class APIUpdate(BaseModel):
    name: str
    url: str

class APIStatus(BaseModel):
    is_active: bool