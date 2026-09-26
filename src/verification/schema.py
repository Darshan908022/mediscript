"""
Data models and schemas for MediScript verification engine.
Defines contracts between Extraction (Member 1), Verification (Team Lead), and UI (Member 2).
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class StatusEnum(str, Enum):
    VERIFIED = "VERIFIED"
    NEEDS_CONFIRMATION = "NEEDS_CONFIRMATION"
    REFUSED = "REFUSED"


class ExtractedMedication(BaseModel):
    id: str = Field(..., description="Unique identifier for the medication item")
    raw_text: str = Field(..., description="Original raw snippet from OCR")
    medicine_name: Optional[str] = Field(None, description="Extracted medicine brand/generic name")
    dose: Optional[str] = Field(None, description="Dose quantity, e.g., '500mg', '1 tablet'")
    frequency: Optional[str] = Field(None, description="Frequency shorthand, e.g., 'BD', 'TDS', 'Once daily'")
    duration: Optional[str] = Field(None, description="Duration, e.g., '5 days', '1 month'")
    timing_instructions: Optional[str] = Field(None, description="Food instructions e.g., 'After food', 'Before bed'")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction or OCR confidence score (0.0 to 1.0)")
    ocr_uncertainty_flag: bool = Field(default=False, description="Flagged true if OCR detected illegible/blurry text")


class VerifiedMedication(ExtractedMedication):
    status: StatusEnum = Field(default=StatusEnum.VERIFIED)
    refusal_reason: Optional[str] = Field(None, description="Reason if item was flagged or refused")
    action_required: Optional[str] = Field(None, description="Guidance prompt for the patient or doctor")
    normalized_frequency: Optional[str] = Field(None, description="Standardized plain text frequency e.g., 'Twice daily (Morning & Evening)'")


class MedicalSummaryExtraction(BaseModel):
    patient_name: Optional[str] = None
    discharge_date: Optional[str] = None
    medications: List[ExtractedMedication] = []
    follow_up_instructions: Optional[str] = None
    warning_signs: List[str] = []


class VerifiedMedicalSummary(BaseModel):
    patient_name: Optional[str] = None
    discharge_date: Optional[str] = None
    medications: List[VerifiedMedication] = []
    follow_up_instructions: Optional[str] = None
    warning_signs: List[str] = []
    overall_status: StatusEnum = Field(default=StatusEnum.VERIFIED)
    refusal_summary: List[str] = []