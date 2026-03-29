"""
=============================================================================
CONFTEST.PY - Pytest Configuration
=============================================================================
This file contains pytest configuration and fixtures.

What is this file for?
- Configure pytest behavior
- Set up logging
- Define fixtures that run before/after tests

Key Concepts:
- "conftest.py" is automatically loaded by pytest
- You don't need to import it - pytest finds it automatically
- Fixtures defined here can be used in any test file
=============================================================================
"""

import pytest
import logging
from datetime import datetime


def pytest_configure(config):
    """
    Configure pytest before test execution.
    
    This function runs once when pytest starts.
    It sets up the HTML report path.
    
    Args:
        config: pytest configuration object
    """
    # Create timestamp for report filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Set the HTML report file path
    # The report will be saved in the reports/ folder
    config.option.htmlpath = f"reports/test_report_{timestamp}.html"


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """
    Set up logging for the entire test session.
    
    - "scope='session'" means this runs ONCE for all tests
    - "autouse=True" means it runs automatically
    
    Logging levels (from lowest to highest):
    - DEBUG: Detailed information for debugging
    - INFO: General information about program execution
    - WARNING: Something unexpected happened, but program continues
    - ERROR: A function failed to perform its task
    - CRITICAL: The program may not be able to continue
    """
    # Configure logging format
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    logger = logging.getLogger("pytest")
    logger.info("=" * 60)
    logger.info("TEST SESSION STARTED")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    yield  # Let tests run
    
    # After all tests complete
    logger.info("=" * 60)
    logger.info("TEST SESSION COMPLETED")
    logger.info("=" * 60)


@pytest.fixture(autouse=True)
def log_test_name(request):
    """
    Log the name of each test before and after it runs.
    
    - "autouse=True" means this runs for EVERY test automatically
    - Shows which test is running in the console/log
    """
    test_name = request.node.nodeid
    logger = logging.getLogger("test")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"STARTING TEST: {test_name}")
    logger.info(f"{'='*60}")
    
    yield  # Let the test run
    
    logger.info(f"COMPLETED TEST: {test_name}")
    logger.info(f"{'='*60}\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook that runs after each test to log the result.
    
    This captures whether each test passed or failed
    and logs it for debugging.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Log test result
    logger = logging.getLogger("test.result")
    
    if report.when == "call":
        if report.failed:
            logger.error(f"TEST FAILED: {item.nodeid}")
            if report.longrepr:
                logger.error(f"Error: {report.longrepr}")
        else:
            logger.info(f"TEST PASSED: {item.nodeid}")
