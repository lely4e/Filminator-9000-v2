class MyCustomError(Exception):
    """Custom exception for my program."""

    def __init__(self, message="Something went wrong"):
        super().__init__(message)
