from pydantic import BaseModel
from typing import List

class ScorecardRule(BaseModel):
    field: str  # Field to evaluate (e.g., "age" or "loan_amount")
    operator: str  # Comparison operator (e.g., ">", "<", "=")
    value: float  # The value to compare against
    score: int  # The score assigned if the condition is satisfied
    
class CreditData(BaseModel):
    age: int
    loan_amount: float