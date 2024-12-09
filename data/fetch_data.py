from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from utils.dynamodb import get_dynamodb_client
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

fetch_bp = Blueprint("fetch", __name__)
dynamodb = get_dynamodb_client()

@fetch_bp.route("/crop-data", methods=["GET"])
def fetch_crop_data():
    table_name = "myCropDataTable2"
    crop_id = request.args.get("crop_id")  # URL parameter for crop_id

    try:
        if crop_id:
            # Fetch specific crop data
            response = dynamodb.get_item(
                TableName=table_name,
                Key={"crop_id": {"S": crop_id}},
            )
            
            if "Item" not in response:
                return jsonify({"error": "Data not found in DynamoDB"}), 404

            item = response["Item"]
            data = json.loads(item["data"]["S"])
            data["image_url"] = item.get("image_url", {}).get("S", None)
            data["timestamp"] = item.get("timestamp", {}).get("S", None)
            data["crop_id"] = item["crop_id"]["S"]  # Add crop_id to the data object
            return jsonify(data)

        else:
            # Fetch all crops
            response = dynamodb.scan(TableName=table_name)
            items = response.get("Items", [])

            all_data = []
            for item in items:
                data = json.loads(item["data"]["S"])
                data["image_url"] = item.get("image_url", {}).get("S", None)
                data["timestamp"] = item.get("timestamp", {}).get("S", None)
                data["crop_id"] = item["crop_id"]["S"]  # Add crop_id to each data object
                all_data.append(data)

            return jsonify(all_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
