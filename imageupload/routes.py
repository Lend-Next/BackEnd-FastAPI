from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from imageupload.schemas import FileCreate
from imageupload.crud import upload_file_to_s3, save_file_metadata
from typing import Generator

router = APIRouter()

# Constants
S3_FOLDER_TYPE_IDENTITY = "identity-doc"
S3_FOLDER_TYPE_LIVE_PHOTO = "live-photo"
ALLOWED_FILE_TYPES = ["image/png", "image/jpeg", "image/jpg"]
MAX_FILE_SIZE_MB = 5


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_file(file: UploadFile) -> None:
    """Validate file type and size."""
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PNG/JPG/JPEG allowed."
        )
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400, 
            detail=f"File size exceeds {MAX_FILE_SIZE_MB}MB limit."
        )


@router.post("/{folder_type}")
async def upload_file(
    folder_type: str,
    person_id: str,
    file: UploadFile,
    db: Session = Depends(get_db)
):
    """Upload a file to the S3 bucket and save its metadata."""
    # Validate folder type
    if folder_type not in [S3_FOLDER_TYPE_IDENTITY, S3_FOLDER_TYPE_LIVE_PHOTO]:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid folder type. Must be one of: {S3_FOLDER_TYPE_IDENTITY}, {S3_FOLDER_TYPE_LIVE_PHOTO}."
        )

    # Validate file
    validate_file(file)

    # Upload file to S3
    file_uri = upload_file_to_s3(file, person_id, folder_type)

    # Save file metadata to RDS
    file_metadata = FileCreate(
        file_uri=file_uri,
        person_id=person_id,
        document_category=folder_type
    )
    db_file = save_file_metadata(db, file_metadata)

    # Return response
    return {
        "file_id": db_file.id,
        "file_uri": db_file.file_uri,
        "person_id": db_file.person_id,
        "document_category": db_file.document_category
    }
