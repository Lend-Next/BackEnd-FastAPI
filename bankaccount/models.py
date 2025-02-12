from sqlalchemy import Column, String, UUID
from uuid import uuid4
from database import Base

class BankSource(Base):
    __tablename__ = "banksource"

    bank_source_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    source_account_id = Column(String)
    bank_id = Column(String)
    source_access_token = Column(String)
    funding_source_url = Column(String)
    shareable_id = Column(String)
    person_id = Column(String)