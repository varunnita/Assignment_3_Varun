# Smart Service Desk Management System

A command-line IT support desk application written in Python. Support staff can create, view, search and resolve service requests. All data is stored in a JSON file and remains available after the application is closed and restarted.

---

## 1. Problem Statement

A company receives IT support requests from employees for laptop, software, network, password, account and access-related issues. These requests are currently maintained manually, which makes them hard to track and easy to lose.

This project provides a small but properly structured application that records each request, tracks whether it is `OPEN` or `RESOLVED`, and saves every change permanently.

---

## 2. Implemented Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Create Service Request | Accepts Request ID, Employee Name, Issue and Priority. Status is set to `OPEN` automatically. |
| 2 | View All Requests | Lists every saved request as `ID \| Employee \| Issue \| Priority \| Status`. |
| 3 | Search Request | Finds one request by Request ID and displays all its details. |
| 4 | Resolve Request | Changes an `OPEN` request to `RESOLVED` and saves the change. |
| 5 | Persistence | All requests are saved to and loaded from `data/requests.json`. |

**Business rules and validations**

- The same Request ID cannot be created twice.
- Priority must be `LOW`, `MEDIUM` or `HIGH` (case-insensitive input).
- Status can only be `OPEN` or `RESOLVED`; the only transition is `OPEN -> RESOLVED`.
- An already resolved request cannot be resolved again.
- Empty fields are rejected.
- Request IDs are case-insensitive (`sr101` is treated as `SR101`).
- A missing, empty or corrupted JSON file is handled safely without crashing.

---

## 3. Concepts Used

### Object-Oriented Programming (OOP)
- `ServiceRequest` is a class with a constructor, attributes and methods (`resolve()`, `to_dict()`, `from_dict()`, `summary()`, `details()`).
- Behaviour is **encapsulated**: status is changed only through `request.resolve()`, never directly from other layers.

### Exception Handling
- Custom exceptions in `domain/exceptions.py`: `RequestNotFoundError`, `DuplicateRequestError`, `InvalidPriorityError`, `InvalidRequestDataError`, `AlreadyResolvedError`, all inheriting from `ServiceDeskError`.
- `main.py` catches `ServiceDeskError` and prints a friendly message. No bare `except:` is used.
- Invalid menu input is handled with a clear message.

### File Handling
- `FileRepository` reads and writes `data/requests.json` using the `json` module.
- Data is loaded at start-up and saved after every create and resolve operation.
- Missing, empty and corrupted files are handled safely.

### SOLID Principles
- **Single Responsibility:** each component has one job.
  - `ServiceRequest` - domain data and behaviour
  - `RequestService` - application use cases
  - `FileRepository` - JSON reading and writing
  - `main.py` - menu, input and output
- **Dependency Inversion:** `RequestService` depends on the abstract `RequestRepository`, not on a JSON file. `FileRepository` implements that abstraction, so storage can be replaced without changing business logic.

### Basic Domain-Driven Design (DDD)
- **Domain layer:** entity, validation, business rules, exceptions, repository contract.
- **Application layer:** use cases coordinating the domain and the repository.
- **Infrastructure layer:** technical JSON implementation.
- **Presentation:** console interface only.
- Domain logic never opens or writes files.

### Git
- Two branches: `main` and `development`.
- Work done on `development` with multiple meaningful commits, then merged into `main`.

---

## 4. Project Structure

```
smart-service-desk/
|-- domain/
|   |-- __init__.py
|   |-- service_request.py        # ServiceRequest entity and business rules
|   |-- exceptions.py             # Custom exceptions
|   `-- request_repository.py     # Abstract repository (DIP)
|-- application/
|   |-- __init__.py
|   `-- request_service.py        # Use cases
|-- infrastructure/
|   |-- __init__.py
|   `-- file_repository.py        # JSON read/write
|-- data/
|   `-- requests.json             # Persistent storage
|-- main.py                       # Menu and user interaction
|-- README.md
`-- .gitignore
```

**Dependency direction:** `main.py` -> `application` -> `domain` <- `infrastructure`

---

## 5. How to Run

**Requirements:** Python 3.8 or higher. No external packages are needed.

```bash
git clone <repository-url>
cd smart-service-desk
python main.py
```

On some systems use `python3 main.py`.

### Sample session

```
SMART SERVICE DESK SYSTEM
1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit
Enter your choice: 1
Enter Request ID: SR101
Enter Employee Name: Rahul
Enter Issue: Laptop is not starting
Enter Priority (LOW/MEDIUM/HIGH): HIGH
Service Request created successfully.
```

### Persistence test

1. Create `SR101` and resolve it (options 1 and 4).
2. Exit using option 5.
3. Run `python main.py` again.
4. Search `SR101` (option 3). The status is still `RESOLVED`.

---

## 6. Error Handling Examples

| Situation | Message |
|-----------|---------|
| Duplicate Request ID | `Error: Request ID SR101 already exists.` |
| Request not found | `Error: Request SR999 not found.` |
| Invalid priority | `Error: Priority must be LOW, MEDIUM or HIGH.` |
| Resolving a resolved request | `Error: Request SR101 is already RESOLVED.` |
| Invalid menu input | `Invalid choice. Please enter a number from 1 to 5.` |

---

## 7. Branch and Merge Explanation

- `main` holds the stable, final version.
- `development` is the working branch where every feature was built and committed.
- After the application was tested on `development`, it was merged into `main` with `git merge development`, and `main` was pushed to the remote repository.

```bash
git checkout main
git merge development
git push
```

Commit history can be viewed with:

```bash
git log --oneline --graph --all
```

---

## 8. Future Scope

Engineer assignment, filtering and sorting, reports, notifications, and a database-backed repository (possible without changing the domain or application layers because of the repository abstraction).
