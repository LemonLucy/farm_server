from flask import Blueprint, request, jsonify
import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()

control_bp = Blueprint('control', __name__)

# AWS IoT 설정
iot_client = boto3.client('iot-data', region_name=os.getenv("AWS_REGION"))

@control_bp.route('/control', methods=['POST'])
def control_robot():
    command = request.json.get('command')
    
    if not command:
        return jsonify({"error": "No command provided"}), 400

    try:
        # IoT Core로 메시지 발행
        response = iot_client.publish(
            topic="robot/control",
            qos=1,
            payload=json.dumps({"command": command})
        )
        return jsonify({"message": "Command sent successfully", "response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
