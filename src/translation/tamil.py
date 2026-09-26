"""
Tamil Translation module for MediScript.
Converts verified medication schedules and clinical warnings into patient-friendly Tamil text.
"""

from typing import Dict, Any, List
from src.verification.schema import VerifiedMedicalSummary, StatusEnum

# Direct mapping for standard normalized medical frequencies to Tamil
FREQUENCY_TAMIL_MAP = {
    "Once daily (Morning)": "தினம் ஒரு முறை (காலை)",
    "Once daily": "தினம் ஒரு முறை",
    "Twice daily (Morning & Evening)": "தினம் இரண்டு முறை (காலை மற்றும் மாலை)",
    "Three times daily (Morning, Afternoon & Evening)": "தினம் மூன்று முறை (காலை, மதியம் மற்றும் இரவு)",
    "Four times daily": "தினம் நான்கு முறை",
    "At bedtime": "இரவு தூங்கும் முன்",
    "As needed": "தேவைப்படும் போது மட்டும்",
    "Immediately": "உடனடியாக",
    "As directed by physician": "மருத்துவர் கூறியபடி"
}

WARNING_TAMIL_MAP = {
    "Chest pain": "நெஞ்சு வலி",
    "Shortness of breath": "மூச்சுத்திணறல்",
    "Fever": "காய்ச்சல்",
    "Severe headache": "கடுமையான தலைவலி",
    "Dizziness": "தலைச்சுற்றல்",
    "Vomiting": "வாந்தி"
}


def translate_summary_to_tamil(summary: VerifiedMedicalSummary) -> Dict[str, Any]:
    """
    Translates verified medical summary into a Tamil-structured schedule dictionary.
    """
    tamil_medications = []

    for med in summary.medications:
        if med.status == StatusEnum.VERIFIED:
            freq_tamil = FREQUENCY_TAMIL_MAP.get(med.normalized_frequency, med.normalized_frequency or "மருத்துவர் கூறியபடி")
            timing_tamil = "உணவுக்கு பின்" if "after" in (med.timing_instructions or "").lower() else "உணவுக்கு முன்" if "before" in (med.timing_instructions or "").lower() else ""

            tamil_medications.append({
                "medicine_name": med.medicine_name,
                "dose": med.dose,
                "frequency_tamil": freq_tamil,
                "duration": med.duration,
                "timing_tamil": timing_tamil,
                "instruction": f"{med.medicine_name} ({med.dose}) - {freq_tamil} {timing_tamil}".strip()
            })

    tamil_warnings = [WARNING_TAMIL_MAP.get(w, w) for w in summary.warning_signs]

    return {
        "patient_name": summary.patient_name,
        "discharge_date": summary.discharge_date,
        "verified_medications_tamil": tamil_medications,
        "warning_signs_tamil": tamil_warnings,
        "follow_up_tamil": summary.follow_up_instructions or "குறிப்பிட்ட நாளில் மருத்துவரை அணுகவும்"
    }