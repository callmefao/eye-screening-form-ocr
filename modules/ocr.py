class OCREngine:
    """Wrap third-party OCR APIs (Tesseract/EasyOCR)."""

    def __init__(self, config=None) -> None:
        self.config = config

    def recognize(self, image, hints=None):
        """Return recognized text along with optional confidence."""
        pass
