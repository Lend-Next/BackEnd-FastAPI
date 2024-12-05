from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from persons import crud, schemas
from sqlalchemy.exc import DataError

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/all", response_model=list[schemas.PersonResponse])
def get_persons(db: Session = Depends(get_db)):
    return crud.get_persons(db)

@router.get("/id-verification/{person_id}", response_model=schemas.PersonBase)
def get_person_verification_data(person_id: str, db: Session = Depends(get_db)):
    try:
        mock_data = crud.get_person_verification_data(db, str(person_id))
    except DataError:
        raise HTTPException(status_code=400, detail="Invalid UUID format.")
    if not mock_data:
        raise HTTPException(status_code=404, detail="Id Verification Failed.")
    return mock_data

@router.get("/{person_id}", response_model=schemas.PersonResponse)
def get_person(person_id: str, db: Session = Depends(get_db)):
    person = crud.get_person_by_id(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/", response_model=schemas.PersonResponse)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db, person)

@router.put("/{person_id}", response_model=schemas.PersonResponse)
def update_person(person_id: str, person: schemas.PersonUpdate, db: Session = Depends(get_db)):
    updated_person = crud.update_person(db, person_id, person)
    if not updated_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated_person

@router.delete("/{person_id}", response_model=schemas.PersonResponse)
def delete_person(person_id: str, db: Session = Depends(get_db)):
    deleted_person = crud.delete_person(db, person_id)
    if not deleted_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return deleted_person
