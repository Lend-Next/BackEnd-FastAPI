# import boto3
# from botocore.exceptions import NoCredentialsError
# from typing import Optional
# import os

# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# )

# def upload_image_to_s3(file, filename: str, bucket_name: str) -> Optional[str]:
#     try:
#         file_path = f"profile-pic/{filename}"
#         s3_client.upload_fileobj(file, bucket_name, file_path)
#         file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_path}"
#         return file_url
#     except NoCredentialsError:
#         print("Credentials not available.")
#         return None
