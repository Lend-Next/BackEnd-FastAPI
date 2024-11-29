import uuid
from sqlalchemy import  Column, Integer, String,UUID,ForeignKey
from database import Base,engine
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

# Define Person model
class Person(Base):
    __tablename__ = "person"
    person_id = Column(String, primary_key=True, index=True)

    accounts = relationship("GetBankAccount", back_populates="person", lazy="joined")

# Define Agent model
class Agent(Base):
    __tablename__ = "agent"
    agent_id = Column(String, primary_key=True, index=True)
    
    # Relationship to bank accounts
    accounts = relationship("GetBankAccount", back_populates="agent", lazy="joined")


class GetBankAccount(Base):
    __tablename__ = "bankaccount"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id = Column(String, unique=True, index=True)
    account_type = Column(String)
    display_name = Column(String)
    currency = Column(String)
    iban = Column(String)  # Store IBAN
    number = Column(String)  # Store account number
    sort_code = Column(String)  # Store sort code
    swift_bic = Column(String)  # Store SWIFT BIC
    person_id = Column(String, ForeignKey("person.person_id", ondelete="SET NULL"), nullable=True)
    agent_id = Column(String, ForeignKey("agent.agent_id", ondelete="SET NULL"), nullable=True)

    # Relationships
    person = relationship("Person", back_populates="accounts", lazy="joined")
    agent = relationship("Agent", back_populates="accounts", lazy="joined")

Base.metadata.create_all(bind=engine)
