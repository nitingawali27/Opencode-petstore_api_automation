"""
=============================================================================
URLS.PY - API Endpoint URLs
=============================================================================
This file contains all the API endpoint URLs for the Petstore API.

What is this file for?
- Store all API URLs in one place (centralized configuration)
- Make it easy to update URLs if the API changes
- Keep URLs out of test files for cleaner code

How to use:
    from utils.urls import create_user, get_user_by_username
    
    # Use the URL in a request
    response = requests.post(create_user, json=payload, headers=headers)
=============================================================================
"""

# Base URL for the Petstore API
# All other endpoints are built from this base URL
baseUrl = "https://petstore.swagger.io/v2"

# =============================================================================
# USER ENDPOINTS
# =============================================================================
# These endpoints are used for user management operations

# POST /user
# Purpose: Create a new user
# Body: User object with id, username, email, etc.
# Response: {"code": 200, "message": "user_id"}
create_user = f"{baseUrl}/user"

# GET /user/{username}
# Purpose: Get user details by username
# URL Parameter: username - The username to look up
# Response: Full user object
get_user_by_username = f"{baseUrl}/user/{{username}}"

# PUT /user/{username}
# Purpose: Update an existing user
# URL Parameter: username - The username to update
# Body: Updated user object
# Response: {"code": 200, "message": "user_id"}
update_user = f"{baseUrl}/user/{{username}}"

# DELETE /user/{username}
# Purpose: Delete a user
# URL Parameter: username - The username to delete
# Response: {"code": 200, "message": "username"}
delete_user = f"{baseUrl}/user/{{username}}"

# =============================================================================
# NOTE: {{username}} is a placeholder that gets replaced at runtime
# Example: update_user.format(username="john123") 
#          becomes "https://petstore.swagger.io/v2/user/john123"
# =============================================================================
