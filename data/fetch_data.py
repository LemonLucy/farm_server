#데이터 조회
from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required
from utils.dynamodb import get_dynamodb_client
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

fetch_bp = Blueprint("fetch", __name__)
dynamodb = get_dynamodb_client()

#@jwt_required()
@fetch_bp.route("/crop-data", methods=["GET"])
def fetch_crop_data():
    table_name = "myCropDataTable"
    crop_id = request.args.get("crop_id")  # URL 파라미터로 crop_id 받아오기

    try:
        if crop_id:
            # 특정 작물 조회
            response = dynamodb.get_item(
                TableName=table_name,
                Key={"crop_id": {"S": crop_id}},
            )
            
            if "Item" not in response:
                return jsonify({"error": "Data not found in DynamoDB"}), 404

            data = response["Item"]["data"]["S"]
            json_data = json.loads(data)
            return jsonify(json_data)
        
        else:
            # 전체 작물 조회
            response = dynamodb.scan(TableName=table_name)
            items = response.get("Items", [])

            # 각 항목의 'data' 필드를 JSON 형식으로 변환하여 반환
            all_data = [json.loads(item["data"]["S"]) for item in items]
            return jsonify(all_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500