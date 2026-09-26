"""
Core Verification Engine.
Coordinates normalization, safe refusal evaluation, and structures output JSON.
"""

from typing import List, Dict, Any
from src.verification.schema import (
    ExtractedMedication,
    VerifiedMedication,
    MedicalSummaryExtraction,
    VerifiedMedicalSummary,
    StatusEnum,
)
from src.verification.refusal import SafeRefusalChecker


FREQUENCY_MAP = {
    "OD": "Once daily (Morning)",
    "QD": "Once daily",
    "BD": "Twice daily (Morning & Evening)",
    "BID": "Twice daily (Morning & Evening)",
    "TDS": "Three times daily (Morning, Afternoon & Evening)",
    "TID": "Three times daily (Morning, Afternoon & Evening)",
    "QID": "Four times daily",
    "HS": "At bedtime",
    "PRN": "As needed",
    "STAT": "Immediately",
    "Q8H": "Every 8 hours",
    "Q12H": "Every 12 hours",
}


class VerificationEngine:
    def __init__(self):
        self.refusal_checker = SafeRefusalChecker()

    def normalize_frequency(self, frequency_str: str) -> str:
        """Translates medical Latin abbreviations to plain English descriptions."""
        if not frequency_str:
            return "As directed by physician"
        
        clean_freq = frequency_str.strip().upper().replace(".", "")
        return FREQUENCY_MAP.get(clean_freq, frequency_str)

    def verify_medication(self, med: ExtractedMedication) -> VerifiedMedication:
        """Processes a single extracted medication through rules and normalization."""
        status, reason, action = self.refusal_checker.evaluate_medication(med)
        normalized_freq = self.normalize_frequency(med.frequency) if med.frequency else None

        # Pydantic v2 compatible dict dump
        return VerifiedMedication(
            **med.model_dump(),
            status=status,
            refusal_reason=reason,
            action_required=action,
            normalized_frequency=normalized_freq
        )

    def process_summary(self, extraction: MedicalSummaryExtraction) -> VerifiedMedicalSummary:
        """
        Executes complete verification pipeline over the extracted discharge summary.
        """
        verified_meds: List[VerifiedMedication] = []
        refusal_notes: List[str] = []
        has_refusal = False
        has_warning = False

        for med in extraction.medications:
            verified_item = self.verify_medication(med)
            verified_meds.append(verified_item)

            if verified_item.status == StatusEnum.REFUSED:
                has_refusal = True
                refusal_notes.append(f"PAUSED [{verified_item.medicine_name or 'Unknown'}]: {verified_item.refusal_reason}")
            elif verified_item.status == StatusEnum.NEEDS_CONFIRMATION:
                has_warning = True
                refusal_notes.append(f"FLAGGED [{verified_item.medicine_name}]: {verified_item.refusal_reason}")

        # Determine global status
        if has_refusal:
            overall_status = StatusEnum.REFUSED
        elif has_warning:
            overall_status = StatusEnum.NEEDS_CONFIRMATION
        else:
            overall_status = StatusEnum.VERIFIED

        return VerifiedMedicalSummary(
            patient_name=extraction.patient_name,
            discharge_date=extraction.discharge_date,
            medications=verified_meds,
            follow_up_instructions=extraction.follow_up_instructions,
            warning_signs=extraction.warning_signs,
            overall_status=overall_status,
            refusal_summary=refusal_notes
        )