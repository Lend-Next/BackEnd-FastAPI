from pydantic import BaseModel

class EmploymentRequest(BaseModel):
    email: str
    
class EmploymentResponse(BaseModel):
    company_name: str
    result: str
    current_term: int

    class Config:
        orm_mode = True