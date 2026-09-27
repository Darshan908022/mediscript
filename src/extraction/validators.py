def validate_extracted_data(data: dict) -> dict:
    """Validates and normalizes LLM extracted medical fields before rendering."""
    validated = {
        "patient_name": data.get("patient_name", "Unknown Patient"),
        "age": data.get("age", "N/A"),
        "gender": data.get("gender", "N/A"),
        "discharge_date": data.get("discharge_date", "N/A"),
        "medications": [],
        "is_ambiguous": data.get("is_ambiguous", False),
        "refusal_reason": data.get("refusal_reason", ""),
        "paused_items": data.get("paused_items", []),
        "follow_up": data.get("follow_up", "Follow up with primary care physician as advised."),
        "warning_signs": data.get("warning_signs", [])
    }
    
    # Clean and validate individual medication fields
    for med in data.get("medications", []):
        if isinstance(med, dict) and med.get("name"):
            validated["medications"].append({
                "name": med.get("name", "Unspecified Medication"),
                "dose": med.get("dose", "Unspecified Dose"),
                "frequency": med.get("frequency", "As directed"),
                "duration": med.get("duration", "As prescribed"),
                "pill_image": med.get("pill_image", "https://cdn-icons-png.flaticon.com/512/883/883407.png"),
                "proof_note": med.get("proof_note", "Extracted from discharge document source text")
            })
            
    return validated