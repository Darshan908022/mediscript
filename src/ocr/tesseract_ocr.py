"""
OCR module for MediScript.
Handles image preprocessing and text extraction from JPG/PNG images and PDF files
using Tesseract OCR and Poppler.
"""

import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Explicit Windows Binary Paths
TESSERACT_EXE_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_BIN_PATH = r"C:\Users\darha\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

# Configure pytesseract executable path if file exists
if os.path.exists(TESSERACT_EXE_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE_PATH


def extract_text_from_image(file_path: str) -> str:
    """
    Extracts raw text from an image or PDF file using Tesseract OCR and Poppler.
    
    :param file_path: Path to the target image (JPG, PNG) or PDF document.
    :return: Extracted raw text as a string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source document file not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    # Process PDF Documents
    if ext == ".pdf":
        try:
            if os.path.exists(POPPLER_BIN_PATH):
                images = convert_from_path(file_path, poppler_path=POPPLER_BIN_PATH)
            else:
                images = convert_from_path(file_path)

            extracted_text = ""
            for page_num, img in enumerate(images):
                page_text = pytesseract.image_to_string(img)
                extracted_text += f"\n--- Page {page_num + 1} ---\n" + page_text

            return extracted_text.strip()

        except Exception as e:
            raise RuntimeError(f"Error converting PDF file via Poppler/pdf2image: {str(e)}")

    # Process Image Formats (JPG, JPEG, PNG, TIFF)
    try:
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.strip()
    except Exception as e:
        raise RuntimeError(f"Error extracting text from image file: {str(e)}")


if __name__ == "__main__":
    # Test execution block - auto-resolves any image placed in samples/
    samples_dir = "samples"
    test_file_path = os.path.join(samples_dir, "clear_sample_1.png")

    # Fallback to any available image in samples directory if exact file name is not found
    if not os.path.exists(test_file_path) and os.path.exists(samples_dir):
        available_files = [f for f in os.listdir(samples_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf'))]
        if available_files:
            test_file_path = os.path.join(samples_dir, available_files[0])

    if os.path.exists(test_file_path):
        print(f"=== Extracting OCR Text from: {test_file_path} ===")
        text_output = extract_text_from_image(test_file_path)
        print("\n--- Extracted Text Output ---")
        print(text_output)
    else:
        print(f"No valid sample image or PDF found in '{samples_dir}/'. Place a test file in the 'samples/' directory to test.")