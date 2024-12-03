from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from persons import crud, schemas

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

@router.get("/id-verification", response_model=schemas.IdVerificationResponse)
def get_person_mock_data(db: Session = Depends(get_db)):
    mock_data = crud.get_person_mock_data(db)
    if not mock_data:
        raise HTTPException(status_code=404, detail="Id Verification Failed.")
    return {
        "Name": mock_data["Name"],
        "DOB": mock_data["DOB"],
        "ID_Document_Type": mock_data["ID-Document Type"],
        "Gender": mock_data["Gender"],
        "Success_Msg": mock_data["Success Msg"],
    }

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
