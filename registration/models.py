from sqlalchemy import Column, BigInteger, String, Boolean, UUID
from database import Base
from uuid import uuid4

class users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    mobile_number = Column(BigInteger)
    encrypted_enpassword = Column(String)
    user_type = Column(String)
    is_active = Column(Boolean, default=True)

    
# class userResponse(users):
#     id: UUID

#     class Config:
#         orm_mode = True