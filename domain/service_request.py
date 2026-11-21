"""ServiceRequest domain entity: data, validation and business behaviour."""

from domain.exceptions import (
    AlreadyResolvedError,
    InvalidPriorityError,
    InvalidRequestDataError,
)

ALLOWED_PRIORITIES = ("LOW", "MEDIUM", "HIGH")
STATUS_OPEN = "OPEN"
STATUS_RESOLVED = "RESOLVED"


class ServiceRequest:
    """Represents one IT support request raised by an employee."""

    def __init__(self, request_id, employee_name, issue, priority,
                 status=STATUS_OPEN):
        self.request_id = self._clean(request_id, "Request ID").upper()
        self.employee_name = self._clean(employee_name, "Employee Name")
        self.issue = self._clean(issue, "Issue Description")
        self.priority = self._validate_priority(priority)
        self.status = status  # new requests always start as OPEN

    # ---------- validation helpers ----------
    @staticmethod
    def _clean(value, field_name):
        value = str(value).strip()
        if not value:
            raise InvalidRequestDataError(f"{field_name} cannot be empty.")
        return value

    @staticmethod
    def _validate_priority(priority):
        priority = str(priority).strip().upper()
        if priority not in ALLOWED_PRIORITIES:
            raise InvalidPriorityError(
                "Priority must be LOW, MEDIUM or HIGH."
            )
        return priority

    # ---------- business behaviour ----------
    def resolve(self):
        """Business rule: OPEN -> RESOLVED. Resolving twice is not allowed."""
        if self.status == STATUS_RESOLVED:
            raise AlreadyResolvedError(
                f"Request {self.request_id} is already RESOLVED."
            )
        self.status = STATUS_RESOLVED

    def is_open(self):
        return self.status == STATUS_OPEN

    # ---------- conversion (plain data, no file access) ----------
    def to_dict(self):
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["request_id"],
            data["employee_name"],
            data["issue"],
            data["priority"],
            data.get("status", STATUS_OPEN),
        )

    def summary(self):
        return (f"{self.request_id} | {self.employee_name} | "
                f"{self.issue} | {self.priority} | {self.status}")

    def details(self):
        return (
            f"Request ID    : {self.request_id}\n"
            f"Employee Name : {self.employee_name}\n"
            f"Issue         : {self.issue}\n"
            f"Priority      : {self.priority}\n"
            f"Status        : {self.status}"
        )
