"""Application layer: use cases of the Smart Service Desk."""

from domain.exceptions import DuplicateRequestError, RequestNotFoundError
from domain.service_request import ServiceRequest


class RequestService:
    def __init__(self, repository):
        self._repository = repository
        self._requests = {r.request_id: r for r in repository.load_all()}

    @staticmethod
    def _normalise(request_id):
        return str(request_id).strip().upper()

    def create_request(self, request_id, employee_name, issue, priority):
        request = ServiceRequest(request_id, employee_name, issue, priority)
        if request.request_id in self._requests:
            raise DuplicateRequestError(
                f"Request ID {request.request_id} already exists."
            )
        self._requests[request.request_id] = request
        self._repository.save_all(list(self._requests.values()))
        return request

    def view_requests(self):
        return list(self._requests.values())

    def search_request(self, request_id):
        key = self._normalise(request_id)
        if key not in self._requests:
            raise RequestNotFoundError(f"Request {key} not found.")
        return self._requests[key]

    def resolve_request(self, request_id):
        request = self.search_request(request_id)
        request.resolve()  # business rule lives in the domain
        self._repository.save_all(list(self._requests.values()))
        return request
