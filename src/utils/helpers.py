import json

def format_patient_summary_text(data: dict) -> str:
    """Formats patient discharge record into a clean downloadable summary for caregivers."""
    summary = f"""MEDISCRIPT PATIENT RECOVERY PLAN
---------------------------------
Patient: {data.get('patient_name')} ({data.get('age')} / {data.get('gender')})
Discharge Date: {data.get('discharge_date')}

VERIFIED MEDICATIONS:
"""
    for m in data.get('medications', []):
        summary += f"- {m.get('name')} {m.get('dose')} | {m.get('frequency')} | Duration: {m.get('duration')}\n"

    summary += f"\nFOLLOW-UP: {data.get('follow_up')}\n"
    summary += f"\nTAMIL INSTRUCTIONS:\n{data.get('tamil_guide')}\n"
    return summary