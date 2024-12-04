from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date

class PersonBase(BaseModel):
    person_name: Optional[str]
    applicant_id: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    date_of_birth: Optional[date]
    marital_status: Optional[str]
    gender: Optional[str]
    house_flat_no: Optional[str]
    street: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    state: Optional[str]
    country: Optional[str]
    current_house_flat_no: Optional[str]
    current_street: Optional[str]
    current_city: Optional[str]
    current_postal_code: Optional[str]
    current_state: Optional[str]
    current_country: Optional[str]
    no_of_dependents: Optional[int]
    time_at_current_address: Optional[int]
    verified_user: Optional[bool]
    user_id: Optional[str]

class PersonCreate(PersonBase):
    pass

class PersonUpdate(PersonBase):
    pass

class PersonResponse(PersonBase):
    person_id: UUID

    class Config:
        orm_mode = True

class IdVerificationResponse(BaseModel):
    Name: str
    DOB: str
    ID_Document_Type: str
    Gender: str
    Success_Msg: str

    class Config:
        orm_mode = True
