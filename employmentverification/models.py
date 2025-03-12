from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import date
from database import Base, engine

from sqlalchemy.sql import func

class EmploymentVerification(Base):
    __tablename__ = "employment_verification"

    employee_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    employer_name = Column(String, nullable=False, default="CloudKaptan Consultancy Services Private Limited")
    designation = Column(String, nullable=False, default="Software Engineer")
    start_date = Column(Date, nullable=False, default=func.current_date())  # Ensure default is a valid date
    employer_address = Column(String, nullable=False, default="Mani Casadona, New Town, Kolkata")


Base.metadata.create_all(bind=engine)
