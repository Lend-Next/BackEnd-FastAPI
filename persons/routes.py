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

@router.get("/all")
def get_persons(db: Session = Depends(get_db)):
    return crud.get_persons(db)

@router.get("/id-verification/{personId}", response_model=schemas.PersonBase)
def get_person_verification_data(personId: str, db: Session = Depends(get_db)):
    try:
        mock_data = crud.get_person_verification_data(db, str(personId))
    except DataError:
        raise HTTPException(status_code=400, detail="Invalid UUID format.")
    if not mock_data:
        raise HTTPException(status_code=404, detail="Id Verification Failed.")
    return mock_data

@router.get("/{personId}")
def get_person(personId: str, db: Session = Depends(get_db)):
    person = crud.get_person_by_id(db, personId)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/create")
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db, person)

@router.put("/id-verification/{personId}")
def update_person(personId: str, person: schemas.PersonBase, db: Session = Depends(get_db)):
    updated_person = crud.update_person(db, personId, person)
    if not updated_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated_person

@router.delete("/{personId}")
def delete_person(personId: str, db: Session = Depends(get_db)):
    deleted_person = crud.delete_person(db, personId)
    if not deleted_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return str(deleted_person.person_name) + " deleted successfully"
