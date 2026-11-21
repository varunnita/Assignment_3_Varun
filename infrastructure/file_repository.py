"""JSON-file implementation of the request repository."""

import json
import os

from domain.request_repository import RequestRepository
from domain.service_request import ServiceRequest


class FileRepository(RequestRepository):
    def __init__(self, file_path="data/requests.json"):
        self.file_path = file_path

    def load_all(self):
        """Read all requests. A missing, empty or corrupt file gives []."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
            if not content:
                return []
            records = json.loads(content)
            return [ServiceRequest.from_dict(item) for item in records]
        except (json.JSONDecodeError, KeyError, TypeError):
            print("Warning: data file is unreadable. Starting with no requests.")
            return []

    def save_all(self, requests):
        """Write all requests to the JSON file."""
        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([r.to_dict() for r in requests], file, indent=4)
