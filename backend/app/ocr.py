# OCR wrapper (tesseract + pdf2image). In production, swap for Google Vision.
from typing import List
from PIL import Image
import pytesseract
import io
try:
    from pdf2image import convert_from_bytes
except Exception:
    convert_from_bytes = None

def run_ocr(file_bytes: bytes, content_type: str) -> List[str]:
    if content_type == 'application/pdf' and convert_from_bytes:
        pages = convert_from_bytes(file_bytes)
        lines = []
        for p in pages:
            text = pytesseract.image_to_string(p)
            lines.extend(text.splitlines())
        return lines
    else:
        img = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(img)
        return text.splitlines()
