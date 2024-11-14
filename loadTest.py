from flask import Flask, jsonify
import boto3
import os
from dotenv import load_dotenv
import json

# 환경 변수 로드
load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

app = Flask(__name__)

# DynamoDB 클라이언트 초기화
dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

@app.route('/fetch-crop-data', methods=['GET'])
def fetch_crop_data():
    table_name = 'myCropDataTable'
    crop_id = 'unique_id_for_crop'  # 실제 데이터의 고유 ID로 대체

    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'crop_id': {'S': crop_id}
            }
        )
        
        # 데이터가 존재하는지 확인
        if 'Item' not in response:
            print("DynamoDB에서 데이터를 가져오지 못했습니다.")
            return jsonify({"error": "Data not found in DynamoDB"}), 404

        # DynamoDB 데이터에서 'data' 필드 추출
        data = response['Item']['data']['S']
        json_data = json.loads(data)  # JSON 문자열을 파싱하여 Python 딕셔너리로 변환
        return jsonify(json_data)

    except Exception as e:
        print("오류 발생:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
