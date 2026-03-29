"""
=============================================================================
PAYLOADS.PY - Test Data Generation
=============================================================================
This file contains functions to generate random user data for testing.

What is this file for?
- Generate realistic random user data for each test run
- Store global test data (like username) shared between tests
- Keep test data generation logic in one place

Key Concepts:
- Payload: The data sent in the request body (JSON format)
- GLOBAL_DATA: A dictionary shared across tests to pass data
- Random data: Ensures each test run creates unique users

How to use:
    from utils.payloads import generate_payload, GLOBAL_DATA
    
    # Generate a new user payload
    payload = generate_payload()
    
    # Store username for later tests
    GLOBAL_DATA["username"] = payload["username"]
    
    # Get username in another test
    username = GLOBAL_DATA.get("username")
=============================================================================
"""

import requests
import string
import pytest
import random
import json

# =============================================================================
# GLOBAL DATA STORAGE
# =============================================================================
# This dictionary is shared across all tests in the session
# Use it to pass data between dependent tests
# 
# Example:
# - Test 1 creates a user and stores username in GLOBAL_DATA
# - Test 2 retrieves the username from GLOBAL_DATA to get that user
GLOBAL_DATA = {}

# =============================================================================
# NAME LISTS
# =============================================================================
# Lists of realistic names to generate random users

# Common first names for generating test users
first_names = ["John", "Alice", "Robert", "Emily", "Michael", "Sophia"]

# Common last names for generating test users
last_names = ["Smith", "Brown", "Johnson", "Davis", "Wilson", "Taylor"]


# =============================================================================
# RANDOM DATA GENERATOR FUNCTIONS
# =============================================================================
# Each function generates a specific piece of random user data

def random_first_name():
    """
    Generate a random first name from the list.
    
    Returns:
        str: A random first name (e.g., "John", "Alice")
    """
    return random.choice(first_names)


def random_last_name():
    """
    Generate a random last name from the list.
    
    Returns:
        str: A random last name (e.g., "Smith", "Brown")
    """
    return random.choice(last_names)


def random_username(first, last):
    """
    Generate a unique username from first and last name.
    
    Format: firstname + lastname + random number
    Example: "johnsmith42", "alicebrown87"
    
    Args:
        first (str): First name
        last (str): Last name
        
    Returns:
        str: A unique username
    """
    return f"{first.lower()}{last.lower()}{random.randint(10,99)}"


def random_email(first, last):
    """
    Generate a random email address.
    
    Format: firstname.lastname@yopmail.com
    Example: "john.smith@yopmail.com"
    
    Note: yopmail.com is a disposable email service, great for testing!
    
    Args:
        first (str): First name
        last (str): Last name
        
    Returns:
        str: A random email address
    """
    return f"{first.lower()}.{last.lower()}@yopmail.com"


def random_phone():
    """
    Generate a random 10-digit phone number.
    
    Returns:
        str: A 10-digit phone number (e.g., "5551234567")
    """
    return ''.join(random.choices("0123456789", k=10))


def generate_payload():
    """
    Generate a complete user payload with random data.
    
    This function creates a realistic user object with:
    - Unique ID
    - Unique username
    - First and last name
    - Email address
    - Password
    - Phone number
    - User status
    
    Returns:
        dict: A complete user payload ready for API requests
        
    Example:
        payload = generate_payload()
        # payload = {
        #     "id": 1234,
        #     "username": "johnsmith42",
        #     "firstName": "John",
        #     "lastName": "Smith",
        #     "email": "john.smith@yopmail.com",
        #     "password": "Pwd5678",
        #     "phone": "5551234567",
        #     "userStatus": 1
        # }
    """
    # Generate unique user ID (random number between 1000-9999)
    user_id = random.randint(1000, 9999)
    
    # Generate random name components
    first = random_first_name()
    last = random_last_name()
    
    # Generate unique username and email
    username = random_username(first, last)
    email = random_email(first, last)
    
    # Build the complete payload
    payload = {
        "id": user_id,
        "username": username,
        "firstName": first,
        "lastName": last,
        "email": email,
        "password": f"Pwd{random.randint(1000,9999)}",  # Random password
        "phone": random_phone(),
        "userStatus": 1  # 1 = active user
    }
    
    # Store username in GLOBAL_DATA for use in other tests
    GLOBAL_DATA["username"] = username
    
    # Print the payload for debugging
    print("Create User Payload:\n", json.dumps(payload, indent=4))
    
    return payload
