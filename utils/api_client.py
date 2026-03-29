"""
=============================================================================
API_CLIENT.PY - API Client Helper Class
=============================================================================
This file contains helper functions for making API requests.

What is this file for?
- Provide reusable functions for common API operations
- Simplify API calls in test files
- Handle request/response logging

How to use:
    from utils.api_client import api_get, api_post, api_put, api_delete
    
    # GET request
    response = api_get(url)
    
    # POST request with body
    response = api_post(url, payload)
=============================================================================
"""

import requests
import json
import logging
from utils.headers import headers

# Create a logger for this module
logger = logging.getLogger("api_client")


def api_get(url, params=None):
    """
    Make a GET request to the API.
    
    GET requests are used to retrieve data from the server.
    They don't modify any data.
    
    Args:
        url (str): The API endpoint URL
        params (dict): Optional query parameters
        
    Returns:
        requests.Response: The response object
        
    Example:
        response = api_get("https://api.example.com/users")
        data = response.json()
    """
    logger.info(f"GET Request: {url}")
    
    response = requests.get(url, headers=headers, params=params)
    
    logger.info(f"Response Status: {response.status_code}")
    return response


def api_post(url, payload):
    """
    Make a POST request to the API.
    
    POST requests are used to create new resources on the server.
    The payload contains the data for the new resource.
    
    Args:
        url (str): The API endpoint URL
        payload (dict): The request body data (will be converted to JSON)
        
    Returns:
        requests.Response: The response object
        
    Example:
        payload = {"name": "John", "email": "john@example.com"}
        response = api_post("https://api.example.com/users", payload)
    """
    logger.info(f"POST Request: {url}")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, headers=headers, json=payload)
    
    logger.info(f"Response Status: {response.status_code}")
    return response


def api_put(url, payload):
    """
    Make a PUT request to the API.
    
    PUT requests are used to update/replace an existing resource.
    The payload contains the complete updated resource data.
    
    Args:
        url (str): The API endpoint URL
        payload (dict): The updated resource data
        
    Returns:
        requests.Response: The response object
        
    Example:
        payload = {"name": "John Updated", "email": "john.updated@example.com"}
        response = api_put("https://api.example.com/users/john", payload)
    """
    logger.info(f"PUT Request: {url}")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.put(url, headers=headers, json=payload)
    
    logger.info(f"Response Status: {response.status_code}")
    return response


def api_delete(url):
    """
    Make a DELETE request to the API.
    
    DELETE requests are used to remove a resource from the server.
    No request body is needed.
    
    Args:
        url (str): The API endpoint URL
        
    Returns:
        requests.Response: The response object
        
    Example:
        response = api_delete("https://api.example.com/users/john")
    """
    logger.info(f"DELETE Request: {url}")
    
    response = requests.delete(url, headers=headers)
    
    logger.info(f"Response Status: {response.status_code}")
    return response
