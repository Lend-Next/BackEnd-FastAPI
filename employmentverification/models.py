import uuid
from sqlalchemy import  Column, Integer, String,UUID
from database import Base,engine
from uuid import uuid4
from sqlalchemy import create_engine


class employmentverification(Base):
    
    __tablename__ = "employmentverification"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    mail = Column(String, unique=True, index=True)
    company_name = Column(String, nullable=False)
    result = Column(String, nullable=False)
    current_term = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

    
