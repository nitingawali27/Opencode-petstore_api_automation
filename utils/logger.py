"""
LOGGER.PY - API Request/Response Logger
Provides detailed logging for all API calls.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional


class APILogger:
    """Handles detailed API request/response logging."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(log_dir, f"api_log_{timestamp}.log")
        self.request_count = 0
        self._setup_logger()
        
        self.logger.info("=" * 80)
        self.logger.info("API TEST SESSION STARTED")
        self.logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Log File: {self.log_file}")
        self.logger.info("=" * 80)
    
    def _setup_logger(self):
        self.logger = logging.getLogger("api_logger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S'))
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _get_request_id(self) -> str:
        self.request_count += 1
        timestamp = datetime.now().strftime('%H%M%S')
        return f"REQ-{timestamp}-{self.request_count:03d}"
    
    def _format_json(self, data: Any) -> str:
        if data is None:
            return "None"
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
                return json.dumps(parsed, indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                return data
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=4, ensure_ascii=False)
        return str(data)
    
    def _format_headers(self, headers: Dict) -> str:
        if not headers:
            return "None"
        formatted = []
        for key, value in headers.items():
            if key.lower() in ['authorization', 'api-key', 'token']:
                masked_value = value[:10] + "..." if len(value) > 10 else "***"
                formatted.append(f"  {key}: {masked_value}")
            else:
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)
    
    def log_request(self, url: str, method: str, headers: Optional[Dict] = None, 
                    payload: Optional[Any] = None, params: Optional[Dict] = None) -> str:
        request_id = self._get_request_id()
        
        log_entry = f"""
{'='*80}
>>> REQUEST: {request_id}
{'='*80}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Method:    {method.upper()}
URL:       {url}

HEADERS:
{self._format_headers(headers)}

PAYLOAD:
{self._format_json(payload)}

"""
        if params:
            log_entry += f"QUERY PARAMETERS:\n{self._format_json(params)}\n"
        
        log_entry += f"{'='*80}"
        self.logger.info(log_entry)
        
        print(f"\n{'='*60}")
        print(f"[REQUEST] {method.upper()} {url}")
        print(f"{'='*60}")
        if payload:
            print(f"Payload:\n{self._format_json(payload)}")
        
        return request_id
    
    def log_response(self, request_id: str, status_code: int, headers: Optional[Dict] = None,
                     body: Optional[Any] = None, elapsed_time: Optional[float] = None):
        if 200 <= status_code < 300:
            status_label = "SUCCESS"
        elif 400 <= status_code < 500:
            status_label = "CLIENT ERROR"
        elif status_code >= 500:
            status_label = "SERVER ERROR"
        else:
            status_label = "INFO"
        
        elapsed_str = f"{elapsed_time:.3f}s" if elapsed_time else "N/A"
        
        log_entry = f"""

<<< RESPONSE: {request_id}
{'='*80}
Timestamp:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status Code:   {status_code} [{status_label}]
Response Time: {elapsed_str}

RESPONSE HEADERS:
{self._format_headers(headers)}

RESPONSE BODY:
{self._format_json(body)}

{'='*80}
"""
        self.logger.info(log_entry)
        
        print(f"\n[RESPONSE] {status_code} [{status_label}]")
        print(f"Time: {elapsed_str}")
        print(f"{'='*60}")
        if body:
            print(f"Body:\n{self._format_json(body)}")
        print(f"{'='*60}\n")
    
    def log_error(self, request_id: str, error: Exception):
        log_entry = f"""

!!! ERROR: {request_id}
{'='*80}
Timestamp:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Error Type: {type(error).__name__}
Message:    {str(error)}
{'='*80}
"""
        self.logger.error(log_entry)
        print(f"\n[ERROR] {type(error).__name__}: {str(error)}\n")
    
    def log_separator(self, title: str = ""):
        if title:
            separator = f"\n\n{'#'*80}\n{'#'*30} {title} {'#'*30}\n{'#'*80}\n"
        else:
            separator = f"\n\n{'#'*80}\n"
        self.logger.info(separator)
        print(separator)
    
    def log_session_end(self):
        log_entry = f"""

{'='*80}
API TEST SESSION COMPLETED
{'='*80}
Timestamp:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Requests: {self.request_count}
Log File:       {self.log_file}
{'='*80}
"""
        self.logger.info(log_entry)
        print(f"\n[SESSION END] Total requests: {self.request_count}")
        print(f"Log saved to: {self.log_file}")


api_logger = APILogger()
