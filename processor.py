import os
import base64
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_receipt_data(file_content):
    # Convert uploaded file bytes to Base64 for Groq
    base64_image = base64.b64encode(file_content).decode('utf-8')

    prompt = """
    Analyze this receipt image. Extract: Merchant Name, Date, Total Amount, Currency, and Category.
    Return the result ONLY as a valid JSON object. 
    Format: {"merchant": "", "date": "YYYY-MM-DD", "total": 0.00, "currency": "", "category": ""}
    """

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(completion.choices[0].message.content)