from pydantic import BaseModel

# Define input schema for user input
class CreditData(BaseModel):
    age: int
    income: float