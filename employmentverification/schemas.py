from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date

class EmploymentRequest(BaseModel):
    email: EmailStr

class EmploymentResponse(BaseModel):
    employeeId: UUID
    email: EmailStr
    employerName: str
    designation: str
    startDate: date
    employerAddress: str

    class Config:
        from_attributes = True  # Newer Pydantic 2.x
