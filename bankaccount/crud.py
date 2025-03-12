# from fastapi import Depends

from sqlalchemy.orm import Session
from bankaccount.models import BankSource
from bankaccount.schemas import BankSourceCreate
# from persons.routes import get_db

def create_bank_source(banksource: BankSourceCreate, db: Session):
    db_banksource = BankSource(source_account_id=banksource.sourceAccountId, 
                           bank_id=banksource.bankId, 
                           source_access_token=banksource.sourceAccessToken, 
                           funding_source_url=banksource.fundingSourceUrl,
                           shareable_id=banksource.shareableId,
                           person_id=banksource.personId)
    db.add(db_banksource)
    db.commit()
    db.refresh(db_banksource)
    return {
        'bankSourceId' : db_banksource.bank_source_id
    }

def get_bank_details(db: Session, personId: str):
    return db.query(BankSource).filter(BankSource.person_id == personId).first()