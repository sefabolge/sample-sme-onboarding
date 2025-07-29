# Example of documents check

import cv2
import pytesseract
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Return True if the image is not blurry (above threshold).
def is_clear_image(path: str, threshold: float = 100.0) -> bool:
    try:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        return cv2.Laplacian(img, cv2.CV_64F).var() > threshold
    except Exception:
        return True  
    
# Return True if OCR output contains all given keywords.
def contains_keywords(path: str, keywords: list[str]) -> bool:
    try:
        text = pytesseract.image_to_string(Image.open(path)).lower()
        return all(keyword in text for keyword in keywords)
    except Exception:
        return False