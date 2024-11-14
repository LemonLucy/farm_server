from flask import Blueprint, request, jsonify
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize AWS Cognito client
cognito_client = boto3.client(
    'cognito-idp',
    region_name=os.getenv("AWS_REGION")
)

auth_bp = Blueprint('auth', __name__)

# User Sign-up Route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # Receive signup data
        email = request.json.get('email')
        password = request.json.get('password')
        
        # Register the user in Cognito
        response = cognito_client.sign_up(
            ClientId=os.getenv("COGNITO_APP_CLIENT_ID"),
            Username=email,
            Password=password,
        )
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# User Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        # Authenticate user in Cognito
        response = cognito_client.initiate_auth(
            ClientId=os.getenv("COGNITO_APP_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
            },
        )
        return jsonify(response['AuthenticationResult']), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
