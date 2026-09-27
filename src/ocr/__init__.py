"""MediScript OCR Package"""
from .tesseract_ocr import extract_text_tesseract
from .vision_ocr import extract_text_vision

__all__ = ["extract_text_tesseract", "extract_text_vision"]