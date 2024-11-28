from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.dynamodb import get_dynamodb_client
from data.openai_integration import analyze_image
import json

upload_bp = Blueprint("upload", __name__)
dynamodb = get_dynamodb_client()

# 작물 이름과 ID 매핑 (기존 작물)
CROP_ID_MAP = {
    "strawberry": "1",
    "spinach": "2",
    "cabbage": "3", 
    "lettuce": "4",
    "kale": "5",
    "green_onion": "6",
    "broccoli": "7",
    "radish": "8",
    "carrot": "9",
    "chinese_cabbage": "10"
}

def get_or_create_crop_id(crop_name):
    """동적으로 crop_name에 대해 crop_id를 생성하거나 기존 ID 반환"""
    if crop_name not in CROP_ID_MAP:
        # 새로운 crop_id 생성 (기존 맵의 길이 + 1로 설정)
        new_id = str(len(CROP_ID_MAP) + 1)
        CROP_ID_MAP[crop_name] = new_id  # 새로운 crop_name과 ID를 매핑에 추가
    return CROP_ID_MAP[crop_name]

def upload_to_dynamodb(data,crop_name, table_name):
    crop_id = get_or_create_crop_id(crop_name)
    try:
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'crop_id': {'S': crop_id},
                'data': {'S': json.dumps(data)}
            }
        )
        print("Data successfully uploaded to DynamoDB!")
    except Exception as e:
        print("Error uploading data to DynamoDB:", e)

# @jwt_required()
@upload_bp.route("/upload-crop-data", methods=["POST"])
def upload_image():
    request_data = request.get_json()
    imageURL = request_data.get("image_url")

    if not imageURL:
        return jsonify({"error": "image_url is required"}), 400

    json_data = analyze_image(imageURL)
    if json_data:
        crop_name = json_data["crop_information"]["name"].lower()
        table_name = 'myCropDataTable'
        upload_to_dynamodb(json_data,crop_name, table_name)
        return jsonify({"message": "Data processed and uploaded successfully", "data": json_data}), 201
    else:
        return jsonify({"error": "Failed to analyze image"}), 500
