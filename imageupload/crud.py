import boto3
from sqlalchemy.orm import Session
from uuid import uuid4
from imageupload.models import File
from imageupload.schemas import FileCreate
from dotenv import load_dotenv
import os
from botocore.exceptions import ClientError
from fastapi import HTTPException

# Load environment variables from .env file
load_dotenv()

# S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = "ap-south-1"

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,  # Your S3 region
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=boto3.session.Config(signature_version="s3v4")
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
    return f"{s3_key}"

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

def get_file_record(db: Session, person_id: str, document_category: str) -> File:
    """Fetch a file record from the database."""
    file_record = db.query(File).filter(
        File.person_id == person_id,
        File.document_category == document_category
    ).first()

    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found for the given person_id and document_category."
        )
    return file_record

def generate_presigned_url(s3_key: str) -> str:
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": AWS_BUCKET_NAME, "Key": s3_key},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        print('s3_key : ' + s3_key)
        print('presigned_url : ' + presigned_url)
        return presigned_url
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error generating presigned URL: {e}")