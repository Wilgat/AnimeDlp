"""Domain errors for AnimeDlp — map to process exit codes in main only."""


class AnimeDlpError(Exception):
    """User-facing operational failure (unsupported host, CF block, empty extract, …)."""

    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code
