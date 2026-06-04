"""Pytest configuration and fixtures for Playwright tests."""

import pytest
from playwright.sync_api import sync_playwright, Browser


@pytest.fixture(scope="session")
def browser():
    """Create and provide a Playwright browser instance for the test session.

    Yields:
        Browser instance
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False for headed mode
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser):
    """Create and provide a new page for each test.

    Args:
        browser: Browser fixture

    Yields:
        Page instance
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

