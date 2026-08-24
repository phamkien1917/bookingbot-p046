class BookingNotFoundError(LookupError):
    """Raised when a requested booking is not found."""
    pass


class BookingConflictError(ValueError):
    """Raised when there is a scheduling conflict or invalid slot selection."""
    pass


class BookingPermissionError(PermissionError):
    """Raised when user does not have permission to access or modify a booking."""
    pass
