from flask import Flask, send_from_directory
from dotenv import load_dotenv
from auth.routes import auth_bp
from data.fetch_data import fetch_bp
import os
from flask_cors import CORS

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)

# Blueprint 등록
app.register_blueprint(auth_bp, url_prefix="/auth")       # Cognito 인증 관련 엔드포인트
app.register_blueprint(fetch_bp, url_prefix="/fetch")     # 데이터 조회 엔드포인트

@app.route("/")
def home():
    return "Welcome to the Farm Server API"

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)