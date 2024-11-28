import os
from flask import Flask, request,jsonify,Blueprint
import json
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
api_bp = Blueprint("api", __name__)

@api_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    try:
        #lambda에서 받은 이미지 url
        #data=request.get_json()
        #image_url=data.get('image_url')

        #if not image_url:
        #    return jsonify({"error": "Image URL is required"}),400

        # 디버깅 로그
        #print(f"Received image URL: {image_url}")

        image_url = "https://mycropbucket.s3.ap-northeast-2.amazonaws.com/딸기.png"

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
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            temperature=0.0,
        )

        #json데이터 추출
        data = response.choices[0].message.content
        cleaned_data = data.replace("```json", "").replace("```", "").strip()
        json_data = eval(cleaned_data)
        print(json_data)
        return json_data
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
