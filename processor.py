import os
import base64
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_receipt_data(file_content):
    base64_image = base64.b64encode(file_content).decode('utf-8')

    # TASK: Multi-stage prompt for Extraction, Categorization, and Analysis
    prompt = """
    Phase 1: Extraction & Structuring
    Identify Merchant, Date, Total, and line items (name, price, quantity).
    
    Phase 2: Categorization
    Classify each item into one of these: Snacks, Dairy, Meat, Bakery, Household, Personal Care, Electronics, or Other.
    
    Phase 3: Spending Analysis
    Calculate:
    1. Total spending per category.
    2. Percentage of total spending per category.
    3. Identify any 'Anomaly' (e.g., an unusually high price for a single item).

    Phase 4: Financial Advice (LLM Insight)
    As a Financial Advisor, look at this specific spending pattern and provide:
    - One personalized budgeting tip.
    - A recommendation for future savings based on these items.

    Return ONLY a JSON object with this structure:
    {
        "merchant": "",
        "date": "",
        "total": 0.0,
        "items": [{"name": "", "price": 0.0, "qty": 1, "category": ""}],
        "category_totals": {"CategoryName": 0.0},
        "category_percentages": {"CategoryName": "0%"},
        "anomalies": [],
        "financial_advice": ""
    }
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