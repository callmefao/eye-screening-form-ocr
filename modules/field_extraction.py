class TextFieldExtractor:
    """Extract plain text fields (patient info, remarks)."""

    def __init__(self, ocr_engine=None, config=None) -> None:
        self.ocr_engine = ocr_engine
        self.config = config

    def extract(self, regions):
        """Return a dict mapping field names to recognized text."""
        pass
