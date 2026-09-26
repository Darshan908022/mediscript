"""
Main Processing Pipeline Controller.
Connects OCR (Member 1) -> Extraction (Member 1) -> Verification (Team Lead) -> Multilingual/UI (Member 2).
"""

import sys
from pathlib import Path

# Add project root directory to sys.path to prevent ModuleNotFoundError when running directly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import json
from typing import Dict, Any, Tuple
from src.verification.schema import MedicalSummaryExtraction, ExtractedMedication, VerifiedMedicalSummary
from src.verification.engine import VerificationEngine


class MediScriptPipeline:
    def __init__(self):
        self.verification_engine = VerificationEngine()

    def process_document(self, raw_ocr_text: str, extracted_json_data: Dict[str, Any]) -> VerifiedMedicalSummary:
        """
        Executes end-to-end backend pipeline logic.
        
        :param raw_ocr_text: Text produced by OCR stage
        :param extracted_json_data: JSON output dict from LLM extractor
        :return: Final validated, verified Pydantic model ready for frontend consumption
        """
        # Step 1: Parse raw LLM output dictionary into structured schema
        meds_list = []
        for idx, item in enumerate(extracted_json_data.get("medications", [])):
            meds_list.append(
                ExtractedMedication(
                    id=f"med_{idx+1}",
                    raw_text=item.get("raw_text", ""),
                    medicine_name=item.get("medicine_name"),
                    dose=item.get("dose"),
                    frequency=item.get("frequency"),
                    duration=item.get("duration"),
                    timing_instructions=item.get("timing_instructions"),
                    confidence_score=float(item.get("confidence_score", 1.0)),
                    ocr_uncertainty_flag=bool(item.get("ocr_uncertainty_flag", False))
                )
            )

        summary_extraction = MedicalSummaryExtraction(
            patient_name=extracted_json_data.get("patient_name"),
            discharge_date=extracted_json_data.get("discharge_date"),
            medications=meds_list,
            follow_up_instructions=extracted_json_data.get("follow_up_instructions"),
            warning_signs=extracted_json_data.get("warning_signs", [])
        )

        # Step 2: Run Verification Engine & Safe Refusal Logic
        verified_summary = self.verification_engine.process_summary(summary_extraction)

        return verified_summary


# Self-test execution block
if __name__ == "__main__":
    sample_llm_output = {
        "patient_name": "Ramesh Kumar",
        "discharge_date": "2026-09-25",
        "medications": [
            {
                "raw_text": "Tab Metformin 500mg BD x 1 month",
                "medicine_name": "Metformin",
                "dose": "500mg",
                "frequency": "BD",
                "duration": "1 month",
                "confidence_score": 0.98,
                "ocr_uncertainty_flag": False
            },
            {
                "raw_text": "Tab Paracetamol ??? TDS",
                "medicine_name": "Paracetamol",
                "dose": "???",
                "frequency": "TDS",
                "duration": "5 days",
                "confidence_score": 0.45,
                "ocr_uncertainty_flag": True
            }
        ],
        "follow_up_instructions": "Review in Cardiology OPD after 2 weeks",
        "warning_signs": ["Chest pain", "Shortness of breath"]
    }

    pipeline = MediScriptPipeline()
    result = pipeline.process_document(raw_ocr_text="", extracted_json_data=sample_llm_output)
    
    print("=== Pipeline Verification Test Output ===")
    print(json.dumps(result.model_dump(), indent=2))