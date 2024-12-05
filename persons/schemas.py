from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date

class PersonBase(BaseModel):
    personName: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    fatherName: Optional[str]
    email: Optional[str]
    phoneNumber: Optional[str]
    DOB: Optional[date]
    maritalStatus: Optional[str]
    gender: Optional[str]
    houseFlatNo: Optional[str]
    street: Optional[str]
    city: Optional[str]
    postalCode: Optional[str]
    state: Optional[str]
    country: Optional[str]
    currentHouseFlatNo: Optional[str]
    currentStreet: Optional[str]
    currentCity: Optional[str]
    currentPostalCode: Optional[str]
    currentState: Optional[str]
    currentCountry: Optional[str]
    noOfDependents: Optional[int]
    timeAtCurrentAddress: Optional[int]
    verifiedUser: Optional[bool]
    userId: Optional[str]

class PersonCreate(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    userId: Optional[str]

class PersonResponse(BaseModel):
    personId: UUID

    class Config:
        orm_mode = True
