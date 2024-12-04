from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID
from typing import Optional
from datetime import date

class ApplicationBase(BaseModel):
    application_name: Optional [str]  = None
    person_id: Optional [str]
    product_id: Optional [str]
    loan_amount: Optional [Decimal]
    loan_term: Optional [Decimal]
    interest_rate: Optional [Decimal]
    status: Optional [str]
    loan_id: Optional [str]
    instalment_frequency: Optional [str]
    drawdown_date: Optional [date]
    first_instalment_date: Optional [date]
    instalment_amount: Optional [Decimal]
    interest_compounding_frequency: Optional [str]
    current_department_id: Optional [str]
    total_score: Optional [Decimal]
    net_income: Optional [Decimal]
    net_deduction: Optional [Decimal]
    assigned_user_id: Optional [str]

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    application_id: UUID

    class Config:
        orm_mode = True