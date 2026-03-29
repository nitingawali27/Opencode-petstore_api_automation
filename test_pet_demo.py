"""
=============================================================================
TEST_PET_DEMO.PY - Petstore User API Tests
=============================================================================
This file contains tests for the Petstore User API endpoints.

API Endpoints Tested:
1. POST /user - Create a new user
2. GET /user/{username} - Get user by username
3. PUT /user/{username} - Update user
4. DELETE /user/{username} - Delete user

Test Flow (Dependencies):
    test_create_user
          │
          ▼
    test_get_user_by_username
          │
          ▼
    test_update_user
          │
          ▼
    test_delete_user

Key Concepts:
- @pytest.mark.dependency: Makes tests depend on each other
- depends=["create"]: This test runs only after "create" passes
- GLOBAL_DATA: Stores data shared between tests
- pytest.skip(): Skip test if prerequisite data is missing

=============================================================================
"""

import requests
import pytest
import json
import sys
import os

# Import URL endpoints from utils
from utils.urls import create_user, get_user_by_username, update_user, delete_user

# Import headers from utils
from utils.headers import headers

# Import payload generator and global data storage
from utils.payloads import generate_payload, GLOBAL_DATA


# =============================================================================
# TEST 1: CREATE USER
# =============================================================================
# This test must run first - other tests depend on it

@pytest.mark.dependency(name="create")
def test_create_user():
    """
    Test creating a new user via POST /user.
    
    This is the first test in the workflow.
    It creates a user and stores the username for other tests.
    
    Steps:
    1. Generate random user data
    2. Send POST request to create user
    3. Verify the response indicates success
    4. Store username in GLOBAL_DATA for other tests
    """
    # Step 1: Generate a random user payload
    payload = generate_payload()
    
    # Store username globally so other tests can use it
    GLOBAL_DATA["username"] = payload["username"]
    
    # Print payload for debugging
    print("Create User Payload:\n", json.dumps(payload, indent=4))
    print("username:", GLOBAL_DATA["username"])

    # Step 2: Send POST request to create the user
    create_user_response = requests.post(
        create_user,        # URL: https://petstore.swagger.io/v2/user
        json=payload,       # Body: user data as JSON
        headers=headers     # Headers: Content-Type: application/json
    )
    
    # Print response for debugging
    print("Create User Response:\n", json.dumps(create_user_response.json(), indent=4))

    # Step 3: Assertions - verify the response is correct
    # Check HTTP status code (200 = OK)
    assert create_user_response.status_code == 200
    
    # Parse the response body
    response_data = create_user_response.json()
    
    # Check API-specific response fields
    assert response_data["code"] == 200, "Response code should be 200"
    assert response_data["message"] == str(payload["id"]), "Message should contain user ID"
    assert GLOBAL_DATA["username"] == payload["username"], "Username should be stored"


# =============================================================================
# TEST 2: GET USER BY USERNAME
# =============================================================================
# This test depends on test_create_user passing first

@pytest.mark.dependency(depends=["create"])
def test_get_user_by_username():
    """
    Test retrieving a user via GET /user/{username}.
    
    This test depends on test_create_user.
    It uses the username stored by the create test.
    
    Steps:
    1. Get username from GLOBAL_DATA
    2. Send GET request to retrieve user
    3. Verify the user data matches what was created
    """
    # Step 1: Get the username from the previous test
    username = GLOBAL_DATA.get("username")
    
    # If username is not set, skip this test
    if not username:
        pytest.skip("Username not set from previous test")

    # Step 2: Send GET request to retrieve user
    # Note: .format(username=username) replaces {username} in the URL
    # Example: "https://petstore.swagger.io/v2/user/{username}" 
    #       becomes "https://petstore.swagger.io/v2/user/johnsmith42"
    get_user_response = requests.get(
        get_user_by_username.format(username=username),
        headers=headers
    )
    
    # Print response for debugging
    print("Get User Response:\n", json.dumps(get_user_response.json(), indent=4))

    # Step 3: Assertions - verify user data
    assert get_user_response.status_code == 200
    
    user_data = get_user_response.json()
    assert user_data["username"] == username, "Username should match"
    assert "id" in user_data, "User should have an ID"
    assert "email" in user_data, "User should have an email"


# =============================================================================
# TEST 3: UPDATE USER
# =============================================================================
# This test depends on test_create_user (for the username)

@pytest.mark.dependency(name="update", depends=["create"])
def test_update_user():
    """
    Test updating a user via PUT /user/{username}.
    
    This test depends on test_create_user.
    It updates the user with new data.
    
    Steps:
    1. Get username from GLOBAL_DATA
    2. Generate new user data
    3. Send PUT request to update user
    4. Verify the update was successful
    """
    # Step 1: Get the username from the create test
    username = GLOBAL_DATA.get("username")
    
    if not username:
        pytest.skip("Username not set from previous test")

    # Step 2: Generate new payload for update
    new_payload = generate_payload()
    print("Update User Payload:\n", json.dumps(new_payload, indent=4))

    # Step 3: Send PUT request to update the user
    update_user_response = requests.put(
        update_user.format(username=username),  # URL with username
        json=new_payload,                       # New user data
        headers=headers
    )
    
    print("Update User Response:\n", json.dumps(update_user_response.json(), indent=4))

    # Step 4: Assertions - verify update was successful
    assert update_user_response.status_code == 200
    response_data = update_user_response.json()
    assert response_data["code"] == 200, "Response code should be 200"
    assert response_data["message"] == str(new_payload["id"]), "Message should contain new user ID"


# =============================================================================
# TEST 4: DELETE USER
# =============================================================================
# This test depends on test_update_user (last in the chain)

@pytest.mark.dependency(name="delete", depends=["update"])
def test_delete_user():
    """
    Test deleting a user via DELETE /user/{username}.
    
    This test depends on test_update_user.
    It removes the user from the system.
    
    Steps:
    1. Get username from GLOBAL_DATA
    2. Send DELETE request
    3. Verify the deletion was successful
    
    Note: This should be the last test as it removes the user.
    """
    # Step 1: Get the username from previous tests
    username = GLOBAL_DATA.get("username")
    
    if not username:
        pytest.skip("Username not set from previous test")

    # Step 2: Send DELETE request to remove the user
    delete_user_response = requests.delete(
        delete_user.format(username=username),
        headers=headers
    )
    
    print("Delete User Status Code:", delete_user_response.status_code)

    # Step 3: Verify deletion
    # If success (200), check the response body
    if delete_user_response.status_code == 200:
        response_data = delete_user_response.json()
        print("Delete User Response:\n", json.dumps(response_data, indent=4))
        assert response_data["code"] == 200, "Response code should be 200"
        assert response_data["message"] == username, "Message should contain username"
    else:
        # If not successful, fail with detailed error message
        pytest.fail(f"Delete failed! Status: {delete_user_response.status_code}, Body: {delete_user_response.text}")
