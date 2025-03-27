from pydantic import BaseModel, EmailStr
from datetime import date

class EmploymentResponse(BaseModel):
    employeeId: str
    email: EmailStr
    employerName: str
    designation: str
    startDate: date
    employerAddress: str

    class Config:
        from_attributes = True  # Newer Pydantic 2.x
