from pydantic import BaseModel


class GetTokenJsonRequest(BaseModel):
    user_id: str
    password: str


class GetTokenJsonResponse(BaseModel):
    access_token: str
