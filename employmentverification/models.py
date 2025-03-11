from sqlalchemy import Column, Integer, String
from database import Base, engine
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

class EmploymentVerification(Base):
    __tablename__ = "employment_verification"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    mail = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String, nullable=False)
    result = Column(String, nullable=False)
    current_term = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)
