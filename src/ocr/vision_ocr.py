import os

def extract_text_vision(image_path: str) -> str:
    """Secondary fallback OCR engine using Google Cloud Vision API."""
    try:
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description if texts else ""
    except Exception as e:
        print(f"Vision OCR Fallback Note: {e}")
        return ""