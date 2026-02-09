"""
Use these in:
1. Service layer
2. Domain logic
3. Repositories (sparingly/rarely)
"""


from app.core.exceptions.base_exception import AppException

class DomainException(AppException):
    """Base exception for domain-level exceptions."""
    pass

class ConflictException(DomainException):
    """Raised when a conflict occurs, such as duplicate entries."""
    pass

class NotFoundException(DomainException):
    """Raised when a resource is not found."""
    pass

class PermissionDeniedException(DomainException):
    """Raised when user lacks permission."""
    pass

class ValidationException(DomainException):
    """Raised when business validation fails."""
    pass

class ForbiddenException(DomainException):
    """Raised when ownership check fails."""
    pass

class BadRequestException(DomainException):
    """Raised for invalid requests."""
    pass
