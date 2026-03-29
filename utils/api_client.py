"""
API_CLIENT.PY - API Client with Detailed Logging
"""

import requests
import time
from typing import Any, Dict, Optional
from utils.headers import headers
from utils.logger import api_logger


def api_get(url: str, params: Optional[Dict] = None) -> requests.Response:
    """Make a GET request with detailed logging."""
    request_id = api_logger.log_request(url=url, method="GET", headers=headers, params=params)
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, params=params)
        elapsed_time = time.time() - start_time
        
        api_logger.log_response(
            request_id=request_id,
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response.json() if response.content else None,
            elapsed_time=elapsed_time
        )
        return response
    except Exception as e:
        api_logger.log_error(request_id, e)
        raise


def api_post(url: str, payload: Dict) -> requests.Response:
    """Make a POST request with detailed logging."""
    request_id = api_logger.log_request(url=url, method="POST", headers=headers, payload=payload)
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload)
        elapsed_time = time.time() - start_time
        
        api_logger.log_response(
            request_id=request_id,
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response.json() if response.content else None,
            elapsed_time=elapsed_time
        )
        return response
    except Exception as e:
        api_logger.log_error(request_id, e)
        raise


def api_put(url: str, payload: Dict) -> requests.Response:
    """Make a PUT request with detailed logging."""
    request_id = api_logger.log_request(url=url, method="PUT", headers=headers, payload=payload)
    
    try:
        start_time = time.time()
        response = requests.put(url, headers=headers, json=payload)
        elapsed_time = time.time() - start_time
        
        try:
            body = response.json() if response.content else None
        except:
            body = response.text if response.content else None
        
        api_logger.log_response(
            request_id=request_id,
            status_code=response.status_code,
            headers=dict(response.headers),
            body=body,
            elapsed_time=elapsed_time
        )
        return response
    except Exception as e:
        api_logger.log_error(request_id, e)
        raise


def api_delete(url: str) -> requests.Response:
    """Make a DELETE request with detailed logging."""
    request_id = api_logger.log_request(url=url, method="DELETE", headers=headers)
    
    try:
        start_time = time.time()
        response = requests.delete(url, headers=headers)
        elapsed_time = time.time() - start_time
        
        try:
            body = response.json() if response.content else None
        except:
            body = response.text if response.content else None
        
        api_logger.log_response(
            request_id=request_id,
            status_code=response.status_code,
            headers=dict(response.headers),
            body=body,
            elapsed_time=elapsed_time
        )
        return response
    except Exception as e:
        api_logger.log_error(request_id, e)
        raise
