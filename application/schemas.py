from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID
from typing import Optional
from datetime import date

class ApplicationBase(BaseModel):
    application_name: Optional[str] = None
    person_id: Optional[UUID] = None  # Still optional in base, but required in create
    product_id: Optional[str] = None
    loan_amount: Optional[Decimal] = None
    loan_term: Optional[int] = None
    interest_rate: Optional[Decimal] = None
    status: Optional[str] = None
    loan_id: Optional[str] = None
    instalment_frequency: Optional[str] = None
    drawdown_date: Optional[date] = None
    first_instalment_date: Optional[date] = None
    instalment_amount: Optional[Decimal] = None
    interest_compounding_frequency: Optional[str] = None
    current_department_id: Optional[str] = None
    total_score: Optional[Decimal] = None
    net_income: Optional[Decimal] = None
    net_deduction: Optional[Decimal] = None
    assigned_user_id: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    person_id: UUID  # ✅ Required because `nullable=False` in models.py

class ApplicationUpdate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    application_id: UUID  # UUID as per models.py

    class Config:
        orm_mode = True