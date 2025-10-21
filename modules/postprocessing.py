class ResultAssembler:
    """Normalize extracted data and combine into the final record."""

    def __init__(self, config=None) -> None:
        self.config = config

    def assemble(self, text_fields, checkbox_states, tables):
        """Return a single dict representing the patient's record."""
        pass
