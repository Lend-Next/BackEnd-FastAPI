import boto3
import os

# Cognito User Pool Settings
USER_POOL_ID = 'ap-south-1_CMRp1sN4W'
CLIENT_ID = 'hkibiomfmpuh9m0oorc1rknkk'
REGION = 'ap-south-1'
JWT_SECRET= 'your-jwt-secret-key'

cognito_client = boto3.client('cognito-idp',region_name=os.getenv('AWS_REGION', REGION))