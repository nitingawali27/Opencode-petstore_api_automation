# Petstore API Automation

A beginner-friendly Python pytest framework for testing the [Petstore API](https://petstore.swagger.io/).

## Project Structure

```
petstore_api_automation/
├── conftest.py            # Pytest configuration and fixtures
├── pytest.ini             # Pytest settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── utils/
│   ├── __init__.py
│   ├── api_client.py     # API helper functions
│   ├── headers.py        # HTTP headers
│   ├── payloads.py       # Test data generation
│   ├── urls.py           # API endpoint URLs
│   └── variables.py      # Global variables
├── tests/
│   └── test_pet_demo.py  # User API tests
└── reports/              # HTML test reports
```

---

## API Endpoint Sequence

### User Management Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                  USER MANAGEMENT WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  STEP 1: CREATE USER                                                │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │ POST /user                                                │      │
│  │                                                           │      │
│  │ Body: {                                                   │      │
│  │     "id": 1234,                                           │      │
│  │     "username": "johndoe42",                              │      │
│  │     "firstName": "John",                                  │      │
│  │     "lastName": "Doe",                                    │      │
│  │     "email": "john.doe@yopmail.com",                      │      │
│  │     "password": "Pwd1234",                                │      │
│  │     "phone": "5551234567",                                │      │
│  │     "userStatus": 1                                       │      │
│  │ }                                                         │      │
│  │                                                           │      │
│  │ Response: {                                               │      │
│  │     "code": 200,                                          │      │
│  │     "message": "1234"                                     │      │
│  │ }                                                         │      │
│  │                                                           │      │
│  │ NOTE: Save username for next steps                        │      │
│  └──────────────────────────────────────────────────────────┘      │
│                         │                                           │
│                         ▼                                           │
│  STEP 2: GET USER                                                  │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │ GET /user/{username}                                      │      │
│  │                                                           │      │
│  │ URL: /user/johndoe42                                      │      │
│  │                                                           │      │
│  │ Response: {                                               │      │
│  │     "id": 1234,                                           │      │
│  │     "username": "johndoe42",                              │      │
│  │     "firstName": "John",                                  │      │
│  │     "lastName": "Doe",                                    │      │
│  │     "email": "john.doe@yopmail.com",                      │      │
│  │     "password": "Pwd1234",                                │      │
│  │     "phone": "5551234567",                                │      │
│  │     "userStatus": 1                                       │      │
│  │ }                                                         │      │
│  └──────────────────────────────────────────────────────────┘      │
│                         │                                           │
│                         ▼                                           │
│  STEP 3: UPDATE USER                                               │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │ PUT /user/{username}                                      │      │
│  │                                                           │      │
│  │ URL: /user/johndoe42                                      │      │
│  │                                                           │      │
│  │ Body: {                                                   │      │
│  │     "id": 1234,                                           │      │
│  │     "username": "johndoe42",                              │      │
│  │     "firstName": "Jane",      <-- Updated                │      │
│  │     "lastName": "Smith",      <-- Updated                │      │
│  │     "email": "jane.smith@yopmail.com",                    │      │
│  │     "password": "NewPwd123",                              │      │
│  │     "phone": "5559876543",                                │      │
│  │     "userStatus": 1                                       │      │
│  │ }                                                         │      │
│  │                                                           │      │
│  │ Response: {                                               │      │
│  │     "code": 200,                                          │      │
│  │     "message": "1234"                                     │      │
│  │ }                                                         │      │
│  └──────────────────────────────────────────────────────────┘      │
│                         │                                           │
│                         ▼                                           │
│  STEP 4: DELETE USER                                               │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │ DELETE /user/{username}                                   │      │
│  │                                                           │      │
│  │ URL: /user/johndoe42                                      │      │
│  │                                                           │      │
│  │ Response: {                                               │      │
│  │     "code": 200,                                          │      │
│  │     "message": "johndoe42"                                │      │
│  │ }                                                         │      │
│  └──────────────────────────────────────────────────────────┘      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## API Endpoints Reference

| Method | Endpoint | Purpose | Test |
|--------|----------|---------|------|
| `POST` | `/user` | Create a new user | `test_create_user` |
| `GET` | `/user/{username}` | Get user by username | `test_get_user_by_username` |
| `PUT` | `/user/{username}` | Update user | `test_update_user` |
| `DELETE` | `/user/{username}` | Delete user | `test_delete_user` |

---

## Test Dependencies

Tests run in a specific order using `pytest-dependency`:

```
test_create_user (creates user, stores username)
        │
        ▼
test_get_user_by_username (uses stored username)
        │
        ▼
test_update_user (uses stored username)
        │
        ▼
test_delete_user (uses stored username, removes user)
```

If `test_create_user` fails, all subsequent tests are skipped.

---

## Quick Start

### 1. Install Dependencies

```bash
cd "D:\POC\petstore_api_automation"
pip install -r requirements.txt
```

### 2. Run All Tests

```bash
pytest -v
```

### 3. Run Single Test

```bash
pytest tests/test_pet_demo.py::test_create_user -v
```

### 4. Run Without Dependencies (skip order)

```bash
pytest tests/test_pet_demo.py -v --ignore-glob="*dependency*"
```

---

## HTTP Methods Explained

| Method | Purpose | Has Body? | Example |
|--------|---------|-----------|---------|
| `GET` | Retrieve data | No | Get user info |
| `POST` | Create data | Yes | Create new user |
| `PUT` | Update/Replace data | Yes | Update user |
| `DELETE` | Remove data | No | Delete user |

---

## HTTP Status Codes

| Code | Meaning | When You See It |
|------|---------|-----------------|
| `200` | OK | Successful request |
| `201` | Created | Resource created successfully |
| `400` | Bad Request | Invalid request body |
| `404` | Not Found | User doesn't exist |
| `500` | Server Error | API server error |

---

## Configuration

Edit `utils/urls.py` to change the API base URL:

```python
baseUrl = "https://petstore.swagger.io/v2"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Tests skip | Check if dependency test passed |
| `404 Not Found` | User may not exist in API |
| `400 Bad Request` | Check payload format |

---

## Key Files Explained

| File | Purpose |
|------|---------|
| `utils/urls.py` | API endpoint URLs |
| `utils/headers.py` | HTTP headers |
| `utils/payloads.py` | Generate random test data |
| `utils/api_client.py` | Helper functions for API calls |
| `tests/test_pet_demo.py` | User CRUD tests |
| `conftest.py` | Logging and pytest setup |
