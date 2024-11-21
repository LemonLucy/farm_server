from flask import Blueprint, request, jsonify
import boto3
import os
from dotenv import load_dotenv
import hmac
import hashlib
import base64
import time
import uuid

load_dotenv()

email_to_username_map = {}

# Initialize AWS Cognito client
cognito_client = boto3.client(
    'cognito-idp',
    region_name=os.getenv("AWS_REGION")
)

auth_bp = Blueprint('auth', __name__)

# Function to calculate SecretHash
def calculate_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(client_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

# User Sign-up Route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # Receive signup data
        email = request.json.get('email')
        password = request.json.get('password')
        
        #username = email.split('@')[0]
        username = str(uuid.uuid4())

        # 이메일과 username 매핑 저장
        email_to_username_map[email] = username

        # Calculate SecretHash
        secret_hash = calculate_secret_hash(
            username,
            os.getenv("COGNITO_APP_CLIENT_ID"),
            os.getenv("COGNITO_APP_CLIENT_SECRET")
        )

        # Register the user in Cognito
        response = cognito_client.sign_up(
            ClientId=os.getenv("COGNITO_APP_CLIENT_ID"),
            Username=username,
            Password=password,
            SecretHash=secret_hash,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ]
        )

        # Attempt to confirm the user automatically
        for _ in range(3):  # 최대 3번 시도
            try:
                cognito_client.admin_confirm_sign_up(
                    UserPoolId=os.getenv("COGNITO_USER_POOL_ID"),
                    Username=username
                )
                break  # 성공 시 루프 종료
            except cognito_client.exceptions.UserNotFoundException:
                time.sleep(1)  # 1초 대기 후 재시도

        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# User Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        username = email_to_username_map.get(email)

        # Calculate SecretHash
        secret_hash = calculate_secret_hash(
            username,
            os.getenv("COGNITO_APP_CLIENT_ID"),
            os.getenv("COGNITO_APP_CLIENT_SECRET")
        )

        # Authenticate user in Cognito
        response = cognito_client.initiate_auth(
            ClientId=os.getenv("COGNITO_APP_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secret_hash
            },
        )
        return jsonify(response['AuthenticationResult']), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
