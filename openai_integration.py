import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image(imageURL):
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
                            "url": imageURL,
                        },
                    },
                ],
            }
        ],
        temperature=0.0,
    )

    data = response.choices[0].message.content
    cleaned_data = data.replace("```json", "").replace("```", "").strip()
    json_data = eval(cleaned_data)
    return json_data
