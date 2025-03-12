from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/{personId}")
def getBankSourceDetails(personId: str, db: Session = Depends(get_db)):
    result = crud.get_bank_details(db, personId)
    if not result:
        raise HTTPException(status_code=404, detail="Bank Details not found")
    return result

@router.get("/bankDetails/{bankSourceId}")
def getBankDetailsBySource(bankSourceId: str, db: Session = Depends(get_db)):
    result = crud.get_bank_details_from_source_id(db, bankSourceId)
    if not result:
        raise HTTPException(status_code=404, detail="Bank Details not found")
    return result

