from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date

class BankSourceCreate(BaseModel):
    bankSourceId: Optional[str]
    sourceAccountId: Optional[str]
    bankId: Optional[str]
    sourceAccessToken: Optional[str]
    fundingSourceUrl: Optional[str]
    shareableId: Optional[str]
    personId: Optional[str]