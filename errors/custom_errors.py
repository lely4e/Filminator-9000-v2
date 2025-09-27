class MovieInDatabaseError(Exception):
    """Custom exception if movie is already in database."""

    def __init__(self, message="Something went wrong"):
        super().__init__(message)


class NoMovieInApiError(Exception):
    """Custom exception if movie doesn't exist in API."""

    def __init__(self, message="Something went wrong"):
        super().__init__(message)


class MovieNotInDatabaseError(Exception):
    """Custom exception if movie is already in database."""

    def __init__(self, message="Something went wrong"):
        super().__init__(message)


class FailedQueryError(Exception):
    """Custom exception if database query fails."""

    def __init__(self, message="Something went wrong"):
        super().__init__(message)
