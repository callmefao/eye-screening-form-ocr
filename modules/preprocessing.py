class PreprocessingPipeline:
    """Handle denoising, resizing, deskewing, and binarization."""

    def __init__(self, config=None) -> None:
        self.config = config

    def run(self, image):
        """Return enhanced image ready for layout analysis."""
        pass
