#dynamoDB클라이언트 초기화
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_dynamodb_client():
    return boto3.client(
        "dynamodb",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
