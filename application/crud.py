from sqlalchemy.orm import Session
from application.models import Application
from application.schemas import ApplicationCreate, ApplicationUpdate
from sqlalchemy import text

def get_applications(db: Session):
    return db.query(Application).all()

def get_application_by_id(db: Session, app_id: str):
    return db.query(Application).filter(Application.application_id == app_id).first()

def generate_application_name(db: Session) -> str:
    # Get the next value from the sequence
    result = db.execute(text("SELECT nextval('app_name_sequence')"))
    seq_number = result.scalar()  # Get the next number from the sequence
    return f"APP-{seq_number:07d}"

def generate_application_data(db: Session, personid: str):
    application_name = generate_application_name(db)  # Ensure the function runs properly
    return {
        "application_name": application_name,  # Fixed typo
        "person_id": personid,
        "product_id": "",
        "loan_amount": 50000,
        "loan_term": 60,
        "interest_rate": 12.75,
        "status": "Approved",
        "loan_id": "",
        "instalment_frequency": "Monthly",
        "drawdown_date": None,
        "first_instalment_date": None,
        "instalment_amount": 2112.00,
        "interest_compounding_frequency": "",
        "current_department_id": "",
        "total_score": None,
        "net_income": None,
        "net_deduction": None,
        "assigned_user_id": ""
    }


    

def create_application(db: Session, application: ApplicationCreate):
    # Generate the application_name before creating the Application
    application_name = generate_application_name(db)
    
    # Create the Application object, excluding application_name from the model_dump()
    application_dict = application.model_dump(exclude={"application_name"})

    db_app = Application(**application_dict, application_name = application_name)

    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def update_application(db: Session, app_id: str, application: ApplicationUpdate):
    db_app = get_application_by_id(db, app_id)
    if not db_app:
        return None
    for key, value in application.model_dump(exclude_unset=True).items():
        setattr(db_app, key, value)
    db.commit()
    db.refresh(db_app)
    return db_app

def delete_application(db: Session, app_id: str):
    db_app = get_application_by_id(db, app_id)
    if not db_app:
        return None
    db.delete(db_app)
    db.commit()
    return db_app