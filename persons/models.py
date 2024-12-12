from sqlalchemy import Column, String, Integer, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base

class Person(Base):
    __tablename__ = "persons"

    person_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    person_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    date_of_birth = Column(Date)
    marital_status = Column(String)
    gender = Column(String)
    house_flat_no = Column(String)
    street = Column(String)
    city = Column(String)
    postal_code = Column(String)
    state = Column(String)
    country = Column(String)
    current_house_flat_no = Column(String)
    current_street = Column(String)
    current_city = Column(String)
    current_postal_code = Column(String)
    current_state = Column(String)
    current_country = Column(String)
    no_of_dependents = Column(Integer)
    time_at_current_address = Column(Integer)
    verified_user = Column(Boolean)
    user_id = Column(String)