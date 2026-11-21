"""Domain-related exceptions for the Smart Service Desk."""


class ServiceDeskError(Exception):
    """Base class for all application-specific errors."""


class DuplicateRequestError(ServiceDeskError):
    """Raised when a Request ID already exists."""


class RequestNotFoundError(ServiceDeskError):
    """Raised when a Request ID does not exist."""


class InvalidPriorityError(ServiceDeskError):
    """Raised when the priority is not LOW, MEDIUM or HIGH."""


class InvalidRequestDataError(ServiceDeskError):
    """Raised when a mandatory field is empty."""


class AlreadyResolvedError(ServiceDeskError):
    """Raised when an already RESOLVED request is resolved again."""
