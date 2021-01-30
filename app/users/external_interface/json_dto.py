from pydantic import BaseModel


class CreateUserJsonRequest(BaseModel):
    user_id: str
    user_name: str
    hashed_password: str
