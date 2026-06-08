"""Pytest configuration and fixtures for Playwright tests."""

import os
import pytest
from playwright.sync_api import sync_playwright, Browser, Page


@pytest.fixture(scope="session")
def browser():
    """Create and provide a Playwright browser instance for the test session.

    Yields:
        Browser instance
    """
    # Allow CI to run in headless mode by default. Set environment variable
    # HEADLESS to "0"/"false"/"no" to force headed mode when running locally.
    headless_env = os.getenv("HEADLESS", "true").lower()
    headless = headless_env not in ("0", "false", "no")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
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


@pytest.fixture
def authenticated_page(page: Page):
    """Create and provide an authenticated page with user logged in.

    This fixture reuses the existing login implementation to provide
    an authenticated session for tests that require a logged-in user.

    Args:
        page: Playwright Page fixture

    Yields:
        Page instance with authenticated user logged in
    """
    from .login_page import LoginPage
    from .home_page import HomePage

    # Navigate to DemoBlaze
    page.goto("https://www.demoblaze.com/")

    # Perform login
    login_page = LoginPage(page)
    login_page.login("pavanol", "test@123")

    # Wait for login to complete
    page.wait_for_selector("//*[contains(text(), 'Welcome')]", timeout=10000)

    yield page

    # Logout after test completes
    try:
        home_page = HomePage(page)
        if home_page.is_logout_link_visible():
            home_page.click_logout_link()
    except Exception:
        pass


