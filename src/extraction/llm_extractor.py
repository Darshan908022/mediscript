import os
import json
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

# Fetch API Key safely from environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client safely
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = genai.Client()

def extract_medication_data(ocr_text: str) -> dict:
    """
    Parses raw OCR discharge summary text into structured JSON via Google Gemini API.
    Handles clinical safe refusal if doses or frequencies are illegible or missing.
    """
    prompt = f"""
    You are an expert medical AI assistant for MediScript.
    Analyze the following raw OCR text extracted from a hospital discharge summary:

    ---
    {ocr_text}
    ---

    Extract the following information into a structured JSON object:
    1. "patient_name": String (default "N/A" if missing)
    2. "age": Integer or String (default "N/A" if missing)
    3. "gender": String (default "N/A" if missing)
    4. "discharge_date": String (YYYY-MM-DD or DD/MM/YYYY, default "N/A" if missing)
    5. "is_ambiguous": Boolean (Set to true IF ANY medication dosage, frequency, or duration is missing, blurry, incomplete, or illegible)
    6. "refusal_reason": String (If is_ambiguous is true, explain why items were paused for safety)
    7. "paused_items": List of strings (List specific unverified or ambiguous medication names)
    8. "medications": List of objects with fields:
       - "name": Medication name
       - "dose": Dosage (e.g., 500mg)
       - "frequency": Exact timing/frequency (e.g., Twice Daily after food)
       - "duration": Course duration (e.g., 1 Month)
    9. "tamil_guide": String (Clear Tamil translation of verified medication instructions)
    10. "follow_up": String (OPD follow-up instructions)
    11. "warning_signs": List of strings (Emergency symptoms requiring immediate medical care)

    Return ONLY a valid JSON object without markdown formatting.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        # Parse JSON response
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)
        return data

    except Exception as e:
        # Fallback safe error response
        return {
            "patient_name": "N/A",
            "age": "N/A",
            "gender": "N/A",
            "discharge_date": "N/A",
            "is_ambiguous": True,
            "refusal_reason": f"Extraction error: {str(e)}",
            "paused_items": ["All items paused due to API processing error."],
            "medications": [],
            "tamil_guide": "தகவல்களை செயலாக்குவதில் பிழை ஏற்பட்டது.",
            "follow_up": "Consult hospital directly.",
            "warning_signs": ["Contact hospital emergency if experiencing severe symptoms."]
        }