class PlaneError(Exception):
    """Base exception for Plane.so API errors."""
    pass

class AuthenticationError(PlaneError):
    """Raised for authentication-related issues."""
    pass

class NotFoundError(PlaneError):
    """Raised when a requested resource is not found."""
    pass

class ValidationError(PlaneError):
    """Raised for invalid input."""
    pass