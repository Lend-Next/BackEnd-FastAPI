# from fastapi import APIRouter, File, UploadFile, HTTPException
# from .crud import upload_image_to_s3
# from .schemas import ImageUploadResponse
# import os

# router = APIRouter()

# @router.post("/upload-image/", response_model=ImageUploadResponse)
# async def upload_image(file: UploadFile = File(...)):
#     try:
#         # Save the uploaded file temporarily
#         temp_filename = file.filename
#         temp_file_path = f"/tmp/{temp_filename}"

#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(await file.read())
        
#         # Upload the file to S3
#         file_url = upload_image_to_s3(open(temp_file_path, "rb"), temp_filename, os.getenv("AWS_BUCKET_NAME"))
        
#         # Remove temporary file
#         os.remove(temp_file_path)
        
#         if file_url:
#             return ImageUploadResponse(filename=temp_filename, url=file_url)
#         else:
#             raise HTTPException(status_code=400, detail="Failed to upload image to S3.")
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
