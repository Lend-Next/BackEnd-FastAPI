from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from application import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/all-applications", response_model=list[schemas.ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return crud.get_applications(db)

# @router.get("/application-data", response_model=schemas.ApplicationData)
# def get_application_mock_data(db: Session = Depends(get_db)):
#     mock_data = crud.get_application_mock_data(db)
#     if not mock_data:
#         raise HTTPException(status_code=404, detail="Id Verification Failed.")
#     return {
#         "Name": mock_data["Name"],
#         "DOB": mock_data["DOB"],
#         "ID_Document_Type": mock_data["ID-Document Type"],
#         "Gender": mock_data["Gender"],
#         "Success_Msg": mock_data["Success Msg"],
#     }

@router.get("/{app_id}", response_model=schemas.ApplicationResponse)
def get_application(app_id: str, db: Session = Depends(get_db)):
    application = crud.get_application_by_id(db, app_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.get("/createapp/{person_id}", response_model=schemas.ApplicationCreate)
def get_application_data(person_id: str, db: Session = Depends(get_db)):
    application_data = crud.generate_application_data(db, person_id)
    if not application_data:
        raise HTTPException(status_code=404)
    return application_data

@router.post("/create-application", response_model=schemas.ApplicationResponse)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, application)

@router.put("/{app_id}", response_model=schemas.ApplicationResponse)
def update_application(app_id: str, application: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    updated_application = crud.update_application(db, app_id, application)
    if not updated_application:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated_application

@router.delete("/{app_id}", response_model=schemas.ApplicationResponse)
def delete_application(app_id: str, db: Session = Depends(get_db)):
    deleted_application = crud.delete_application(db, app_id)
    if not deleted_application:
        raise HTTPException(status_code=404, detail="Application not found")
    return deleted_application