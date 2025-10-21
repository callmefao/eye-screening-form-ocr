class TableExtractor:
    """Parse metric tables and return structured rows."""

    def __init__(self, ocr_engine=None, config=None) -> None:
        self.ocr_engine = ocr_engine
        self.config = config

    def extract(self, regions):
        """Return list/dict structures representing table contents."""
        pass
