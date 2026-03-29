"""
=============================================================================
TEST_API_WITH_LOGGING.PY - API Tests with Detailed Logging
=============================================================================
This file demonstrates API testing with detailed request/response logging.

Each API call is logged with:
- Unique Request ID
- Request URL, method, headers, payload
- Response status, headers, body (pretty-printed JSON)
- Response time

Log files are saved in the logs/ folder.
=============================================================================
"""

import pytest
import json
from utils.api_client import api_get, api_post, api_put, api_delete
from utils.urls import create_user, get_user_by_username, update_user, delete_user
from utils.payloads import generate_payload, GLOBAL_DATA
from utils.logger import api_logger


class TestAPIWithLogging:
    """Test class demonstrating detailed API logging."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup before each test."""
        # Log test start
        api_logger.log_separator("TEST START")
        yield
        api_logger.log_separator("TEST END")
    
    def test_01_create_user(self):
        """
        Test 1: Create a new user (POST /user)
        
        This test creates a user and logs all request/response details.
        """
        # Generate random user payload
        payload = generate_payload()
        GLOBAL_DATA["username"] = payload["username"]
        
        # Make POST request with automatic logging
        response = api_post(create_user, payload)
        
        # Verify response
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["code"] == 200
        
        print(f"\n✅ User created: {payload['username']}")
    
    def test_02_get_user(self):
        """
        Test 2: Get user by username (GET /user/{username})
        
        This test retrieves user details with full logging.
        """
        username = GLOBAL_DATA.get("username")
        if not username:
            pytest.skip("Username not set from previous test")
        
        # Make GET request with automatic logging
        url = get_user_by_username.format(username=username)
        response = api_get(url)
        
        # Verify response
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["username"] == username
        
        print(f"\n✅ User retrieved: {username}")
    
    def test_03_update_user(self):
        """
        Test 3: Update user (PUT /user/{username})
        
        This test updates user details with full logging.
        """
        username = GLOBAL_DATA.get("username")
        if not username:
            pytest.skip("Username not set from previous test")
        
        # Generate new payload for update
        new_payload = generate_payload()
        
        # Make PUT request with automatic logging
        url = update_user.format(username=username)
        response = api_put(url, new_payload)
        
        # Verify response
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["code"] == 200
        
        print(f"\n✅ User updated: {username}")
    
    def test_04_delete_user(self):
        """
        Test 4: Delete user (DELETE /user/{username})
        
        This test deletes the user with full logging.
        """
        username = GLOBAL_DATA.get("username")
        if not username:
            pytest.skip("Username not set from previous test")
        
        # Make DELETE request with automatic logging
        url = delete_user.format(username=username)
        response = api_delete(url)
        
        # Verify response
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["code"] == 200
        
        print(f"\n✅ User deleted: {username}")
        
        # Log session end after final test
        api_logger.log_session_end()


class TestMultipleAPIs:
    """Test class showing multiple API calls with separate log entries."""
    
    def test_multiple_users(self):
        """
        Test creating multiple users.
        Each API call gets its own detailed log entry.
        """
        api_logger.log_separator("MULTIPLE USERS TEST")
        
        users_created = []
        
        # Create 3 users - each with separate log entry
        for i in range(3):
            api_logger.log_separator(f"Creating User {i+1}")
            
            payload = generate_payload()
            response = api_post(create_user, payload)
            
            if response.status_code == 200:
                users_created.append(payload["username"])
                print(f"✅ User {i+1} created: {payload['username']}")
        
        # Cleanup - delete all created users
        for username in users_created:
            api_logger.log_separator(f"Deleting User: {username}")
            
            url = delete_user.format(username=username)
            response = api_delete(url)
            
            if response.status_code == 200:
                print(f"✅ User deleted: {username}")
        
        api_logger.log_session_end()
