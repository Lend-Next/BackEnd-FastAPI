from pydantic import BaseModel, EmailStr
from typing import Optional

class EmploymentRequest(BaseModel):
    email: str
    
class EmploymentResponse(BaseModel):
    mail: str
    company_name: str
    result: str
    current_term: int