"""
LLM Extraction module for MediScript.
Parses raw OCR text into structured JSON using Google Gemini API.
"""

import os
import json
from typing import Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize Google GenAI Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key) if api_key else genai.Client()

EXTRACTION_PROMPT_TEMPLATE = """
You are an expert medical document parser. Extract prescription and medical summary details from the raw discharge summary text provided below.

Strictly adhere to the following rules:
1. Extract patient_name, discharge_date, follow_up_instructions, warning_signs, and medications list.
2. For each medication, extract:
   - raw_text: exact text snippet describing the medication
   - medicine_name: brand or generic name
   - dose: e.g., '500mg', '1 tablet'
   - frequency: e.g., 'BD', 'TDS', 'OD', 'Once daily'
   - duration: e.g., '5 days', '1 month'
   - timing_instructions: e.g., 'After food', 'At bedtime'
   - confidence_score: float value between 0.0 and 1.0 indicating clarity
   - ocr_uncertainty_flag: true if the dose/text is blurry, incomplete, or contains '???', otherwise false
3. Return ONLY valid JSON adhering to this exact structure:

{{
  "patient_name": "String or null",
  "discharge_date": "YYYY-MM-DD or string or null",
  "medications": [
    {{
      "raw_text": "Tab Metformin 500mg BD x 1 month",
      "medicine_name": "Metformin",
      "dose": "500mg",
      "frequency": "BD",
      "duration": "1 month",
      "timing_instructions": "After food",
      "confidence_score": 0.95,
      "ocr_uncertainty_flag": false
    }}
  ],
  "follow_up_instructions": "String or null",
  "warning_signs": ["String"]
}}

Raw Discharge Text:
\"\"\"
{raw_ocr_text}
\"\"\"
"""


def extract_discharge_data(raw_ocr_text: str) -> Dict[str, Any]:
    """
    Calls Google Gemini API to produce structured JSON from raw OCR text.
    
    :param raw_ocr_text: The plain text produced by OCR.
    :return: Parsed dictionary matching extraction schema.
    """
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(raw_ocr_text=raw_ocr_text)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1,
        )
    )

    try:
        extracted_json = json.loads(response.text)
        return extracted_json
    except json.JSONDecodeError:
        # Fallback handling in case of formatting anomalies
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)


if __name__ == "__main__":
    # Test execution block
    sample_text = """
    DISCHARGE SUMMARY
    Patient Name: Ramesh Kumar
    Date of Discharge: 25/09/2026

    Rx (Medications):
    1. Tab Metformin 500mg BD after food x 1 month
    2. Tab Paracetamol ??? TDS for fever x 5 days

    Follow up: Cardiology OPD after 2 weeks.
    Warning Signs: Seek emergency help if experiencing chest pain or shortness of breath.
    """
    
    print("=== Sending Sample OCR Text to Gemini API ===")
    extracted_data = extract_discharge_data(sample_text)
    print(json.dumps(extracted_data, indent=2))