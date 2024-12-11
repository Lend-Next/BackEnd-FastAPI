from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import FileCreate
from crud import upload_file_to_s3, save_file_metadata
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def upload_file(
    person_id: str,
    file: UploadFile,
    db: Session = Depends(get_db)
):
    # Validate file type
    allowed_types = ["image/png", "image/jpeg", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG/JPG/JPEG allowed.")

    # Validate file size (5MB)
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")

    # Upload file to S3
    file_uri = upload_file_to_s3(file, person_id)

    # Save file metadata to RDS
    file_metadata = FileCreate(
        file_uri=file_uri,
        person_id=person_id
    )
    db_file = save_file_metadata(db, file_metadata)
    return {"file_id": db_file.id, "file_uri": db_file.file_uri, "person_id": db_file.person_id}