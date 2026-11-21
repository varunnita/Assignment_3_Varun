"""Abstract repository contract (Dependency Inversion).

The application layer depends on this abstraction, not on JSON files.
"""

from abc import ABC, abstractmethod


class RequestRepository(ABC):
    @abstractmethod
    def load_all(self):
        """Return a list of ServiceRequest objects."""

    @abstractmethod
    def save_all(self, requests):
        """Persist the given list of ServiceRequest objects."""
