import boto3
from sqlalchemy.orm import Session
from uuid import uuid4
from imageupload.models import File
from imageupload.schemas import FileCreate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
# AWS_REGION = os.getenv("AWS_REGION")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def upload_file_to_s3(file, person_id: str, document_category: str) -> str:
    file_id = str(uuid4())
    file_extension = file.filename.split(".")[-1]
    s3_key = f"{document_category}/{file_id}.{file_extension}"

    s3_client.upload_fileobj(
        file.file,
        AWS_BUCKET_NAME,
        s3_key,
        ExtraArgs={"ContentType": file.content_type}
    )
    return f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

def save_file_metadata(db: Session, file_data: FileCreate) -> File:
    new_file = File(
        id=str(uuid4()),
        file_uri=file_data.file_uri,
        person_id=file_data.person_id,
        document_category=file_data.document_category
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file