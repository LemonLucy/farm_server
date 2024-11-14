from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import boto3
import os

auth_bp = Blueprint("auth", __name__)

# AWS Cognito 설정
#cognito_client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION"))
cognito_client = boto3.client("cognito-idp", region_name="ap-northeast-2")

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    try:
        # Cognito에서 사용자 인증
        response = cognito_client.initiate_auth(
            ClientId=os.getenv("COGNITO_APP_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
        )
        # 인증 성공 시 JWT 토큰 생성
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    except cognito_client.exceptions.NotAuthorizedException:
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
