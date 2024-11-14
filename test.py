from openai import OpenAI
import os
import boto3
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

client = OpenAI(api_key=openai_api_key)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        { 
            "role": "system",
            "content": "You are a plant disease and pest detector"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
                    Analyze this image and provide information about the crop in JSON format only. Respond with JSON data only, and do not include any explanations, comments, or additional formatting. The response must match the following structure exactly:
                    {
                        \"crop_information\": {
                            \"name\": \"string\",
                            \"species\": \"string\",
                            \"growth_stage\": \"string\"
                        },
                        \"pest_information\": {
                            \"pest_name\": \"string\",
                            \"severity\": \"string\",
                            \"pesticide\": \"string\"
                        },
                        \"disease_information\": {
                            \"disease_name\": \"string\",
                            \"symptoms\": \"string\",
                            \"severity\": \"string\",
                            \"pesticide\": \"string\"
                        },
                        \"crop_health_information\": {
                            \"overall_health\": \"string\",
                            \"recommended_action\": \"string\"
                        }
                    }
                    """
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://www.eatingwell.com/thmb/JXv46YsRlGG2HXEBEIfnivRsqx8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/is-It-dafe-to-eat-strawberries-w-fluffy-white-stuff-on-them-1e8627762b6b42bf8418ecbb4415303c.jpg",
                    },
                },
            ],
        }
    ],
    temperature=0.0,
)

data = response.choices[0].message.content
cleaned_data = data.replace("```json", "").replace("```", "").strip()
json_data = eval(cleaned_data)  # Convert string output to JSON (use with caution; ensure response is well-formatted)
print(json_data)

# DynamoDB 클라이언트 초기화
dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# DynamoDB에 JSON 데이터를 업로드하는 함수
def upload_to_dynamodb(data, table_name):
    try:
        # DynamoDB는 JSON 데이터를 넣을 때 딕셔너리 형태로 변환해야 합니다
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'crop_id': {'S': 'unique_id_for_crop'},  # 필요에 따라 고유 ID로 변경
                'data': {'S': json.dumps(data)}  # JSON 데이터를 문자열로 저장
            }
        )
        print("Data successfully uploaded to DynamoDB!")
    except Exception as e:
        print("Error uploading data to DynamoDB:", e)

# DynamoDB 테이블 이름 설정
table_name = 'myCropDataTable'

# 데이터 업로드
upload_to_dynamodb(json_data, table_name)