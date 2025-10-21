class CheckboxDetector:
    """Detect ticked/unticked states in checkbox groups."""

    def __init__(self, config=None) -> None:
        self.config = config

    def detect(self, regions):
        """Return a dict mapping checkbox IDs to boolean states."""
        pass
