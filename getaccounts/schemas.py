from pydantic import BaseModel
from typing import Optional

class PersonBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class AgentBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class GetBankAccountResponse(BaseModel):
    account_id: str
    account_type: str
    display_name: str
    currency: str
    iban: str
    number: str
    sort_code: str
    swift_bic: str
    person_id: Optional[str] = None  # person_id can be null
    agent_id: Optional[str] = None  # agent_id can be null

    class Config:
        orm_mode = True

# Pydantic models for responses
class Person(PersonBase):
    person_id: str

class Agent(AgentBase):
    agent_id: str

class GetBankAccount(GetBankAccountResponse):
    person: Optional[Person] = None  # Optional relationship with Person
    agent: Optional[Agent] = None  # Optional relationship with Agent
