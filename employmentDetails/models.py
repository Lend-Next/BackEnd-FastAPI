from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from database import Base, engine


class EmploymentVerification(Base):
    __tablename__ = "employment_details"

    employment_details_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    employee_id = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    employer_name = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)  # Ensure default is a valid date
    employer_address = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)
