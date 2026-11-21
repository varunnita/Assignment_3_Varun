"""Presentation layer: menu, input and output only."""

from application.request_service import RequestService
from domain.exceptions import ServiceDeskError
from infrastructure.file_repository import FileRepository

MENU = """
SMART SERVICE DESK SYSTEM
1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit"""


def create_request(service):
    request_id = input("Enter Request ID: ")
    employee = input("Enter Employee Name: ")
    issue = input("Enter Issue: ")
    priority = input("Enter Priority (LOW/MEDIUM/HIGH): ")
    service.create_request(request_id, employee, issue, priority)
    print("Service Request created successfully.")


def view_requests(service):
    requests = service.view_requests()
    if not requests:
        print("No service requests available.")
        return
    for request in requests:
        print(request.summary())


def search_request(service):
    request = service.search_request(input("Enter Request ID: "))
    print(request.details())


def resolve_request(service):
    request = service.resolve_request(input("Enter Request ID: "))
    print(f"Request {request.request_id} marked as RESOLVED.")


def main():
    service = RequestService(FileRepository("data/requests.json"))
    actions = {
        "1": create_request,
        "2": view_requests,
        "3": search_request,
        "4": resolve_request,
    }
    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        if choice == "5":
            print("Thank you. Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue
        try:
            action(service)
        except ServiceDeskError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
