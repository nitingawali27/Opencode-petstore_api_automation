"""
=============================================================================
HEADERS.PY - HTTP Request Headers
=============================================================================
This file contains the default HTTP headers used for all API requests.

What is this file for?
- Define common headers used across all requests
- Keep header configuration in one place
- Make it easy to add new headers (like Authorization)

How to use:
    from utils.headers import headers
    
    response = requests.get(url, headers=headers)

Common HTTP Headers:
- Content-Type: Tells the server what format the request body is in
- Accept: Tells the server what format we want the response in
- Authorization: Used for authentication (Bearer token)
=============================================================================
"""

# Default headers for all API requests
# 
# "Content-Type: application/json" means:
# - We are sending JSON data in the request body
# - The server should parse the body as JSON
#
# Note: For some APIs, you might also need:
# - "Accept: application/json" (we want JSON response)
# - "Authorization: Bearer token123" (for authenticated requests)
headers = {
    "Content-Type": "application/json"
}
