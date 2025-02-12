from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from bankaccount import crud, schemas
from typing import Generator

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/banksourcecreate")
def createbanksource(banksource: schemas.BankSourceCreate, db: Session = Depends(get_db)):
    return crud.create_bank_source(banksource, db)

