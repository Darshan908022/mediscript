"""
Safe Refusal Logic for MediScript.
Ensures no ambiguous, missing, or conflicting clinical instructions are guessed.
"""

from typing import List, Tuple, Optional
from src.verification.schema import ExtractedMedication, StatusEnum


class SafeRefusalChecker:
    """Evaluates individual medication extractions against clinical safety rules."""

    MIN_CONFIDENCE_THRESHOLD = 0.70

    @classmethod
    def evaluate_medication(cls, med: ExtractedMedication) -> Tuple[StatusEnum, Optional[str], Optional[str]]:
        """
        Evaluates a medication record and returns (StatusEnum, refusal_reason, action_required).
        """
        # Rule 1: High OCR Uncertainty / Blur
        if med.ocr_uncertainty_flag:
            return (
                StatusEnum.REFUSED,
                "Text image was illegible or blurry in the source document.",
                "Please verify this prescription directly with your hospital or pharmacy before taking."
            )

        # Rule 2: Low Confidence Score
        if med.confidence_score < cls.MIN_CONFIDENCE_THRESHOLD:
            return (
                StatusEnum.NEEDS_CONFIRMATION,
                f"Low extraction confidence score ({med.confidence_score:.2f}).",
                "Please check the original discharge paper to confirm the exact dosage details."
            )

        # Rule 3: Missing Vital Fields (Medicine Name or Dose)
        if not med.medicine_name or not med.medicine_name.strip():
            return (
                StatusEnum.REFUSED,
                "Medication name could not be identified.",
                "Consult your doctor to verify what medication was prescribed."
            )

        if not med.dose or not med.dose.strip():
            return (
                StatusEnum.NEEDS_CONFIRMATION,
                f"Dosage quantity is missing or unclear for '{med.medicine_name}'.",
                "Do not guess the dosage. Confirm with your doctor or pharmacist."
            )

        # Rule 4: Ambiguous or Unrecognized Dosage Notation
        unclear_keywords = ["?", "unknown", "unclear", "check doctor", "null", "none"]
        if any(kw in med.dose.lower() for kw in unclear_keywords) or any(kw in (med.frequency or "").lower() for kw in unclear_keywords):
            return (
                StatusEnum.REFUSED,
                f"Unclear or ambiguous dose/frequency recorded for '{med.medicine_name}'.",
                "Hospital clarification is required. This item has been paused from your schedule."
            )

        # Rule 5: Conflicting or Contradictory Frequency Instructions
        freq = (med.frequency or "").upper().strip()
        if ("ONCE" in freq and "TDS" in freq) or ("BD" in freq and "OD" in freq and "TDS" in freq):
            return (
                StatusEnum.REFUSED,
                f"Conflicting frequency shorthand detected in '{med.raw_text}'.",
                "The prescription contains contradictory timings. Contact your doctor immediately."
            )

        return (StatusEnum.VERIFIED, None, None)