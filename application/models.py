from sqlalchemy import Column, String, Integer, Date, Numeric, Sequence
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base

class Application(Base):
    __tablename__ = "applications"

    application_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    application_name = Column(String)
    person_id = Column(String)
    product_id = Column(String)

    loan_amount = Column(Numeric(precision=12, scale=2))
    loan_term = Column(Integer)
    interest_rate = Column(Numeric(precision=5, scale=4))
    status = Column(String)
    loan_id = Column(String)
    instalment_frequency = Column(String)
    drawdown_date = Column(Date)
    first_instalment_date = Column(Date)
    instalment_amount = Column(Numeric(precision=12, scale=2))
    interest_compounding_frequency = Column(String)

    current_department_id = Column(String)
    total_score = Column(Numeric(precision=12, scale=2))
    net_income = Column(Numeric(precision=12, scale=2))
    net_deduction = Column(Numeric(precision=12, scale=2))

    assigned_user_id = Column(String)
