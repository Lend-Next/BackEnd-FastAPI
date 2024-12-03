from pydantic import BaseModel
from typing import Optional

# Schema to return user info
class UserInfoResponse(BaseModel):
    user_id: str
    email: Optional[str] = None
    username: Optional[str] = None

    class Config:
        orm_mode = True

class UserIdResponse(BaseModel):
    user_id: str

    class Config:
        orm_mode = True
