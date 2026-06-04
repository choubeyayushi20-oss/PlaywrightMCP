"""Login/Logout test for DemoBlaze using Page Object Model."""

import pytest
from playwright.sync_api import Page
from .login_page import LoginPage
from .home_page import HomePage


@pytest.fixture()
def browser_page(page: Page):
    """Fixture to provide a page object with DemoBlaze URL loaded.

    Args:
        page: Playwright Page fixture

    Yields:
        Page object with DemoBlaze loaded
    """
    page.goto("https://www.demoblaze.com/")
    yield page
    page.close()


def test_login_logout(page: Page):
    """Test login and logout functionality on DemoBlaze.

    Test Steps:
    1. Open https://www.demoblaze.com/
    2. Click on "Log in" link in the top navigation bar
    3. Enter "pavanol" in the Username field
    4. Enter "test@123" in the Password field
    5. Click on the "Log in" button
    6. Verify that the "logout link" is visible
    7. Verify that the text "Welcome pavanol" appears at the top right
    8. Click on the "Log out" link
    9. Verify that the "Log in" link is visible again after logout

    Args:
        page: Playwright Page fixture
    """
    # Step 1: Navigate to DemoBlaze
    page.goto("https://www.demoblaze.com/")
    print("✓ Step 1: Navigated to https://www.demoblaze.com/")

    # Initialize page objects
    login_page = LoginPage(page)
    home_page = HomePage(page)

    # Step 2: Click on "Log in" link
    login_page.click_login_link()
    print("✓ Step 2: Clicked on 'Log in' link")

    # Step 3 & 4: Enter username and password
    login_page.enter_username("pavanol")
    print("✓ Step 3: Entered username 'pavanol'")

    login_page.enter_password("test@123")
    print("✓ Step 4: Entered password 'test@123'")

    # Step 5: Click Login button
    login_page.click_login_button()
    print("✓ Step 5: Clicked 'Log in' button")

    # Wait for login to complete (wait for logout link to appear)
    page.wait_for_selector("//a[contains(text(), 'Log out')]", timeout=10000)

    # Step 6: Verify logout link is visible
    assert home_page.is_logout_link_visible(), "Logout link should be visible after login"
    print("✓ Step 6: Logout link is visible")

    # Step 7: Verify welcome message
    assert home_page.verify_welcome_message(
        "pavanol"
    ), "Welcome message should contain 'pavanol'"
    welcome_text = home_page.get_welcome_text()
    print(f"✓ Step 7: Welcome message verified: '{welcome_text}'")

    # Step 8: Click Logout link
    home_page.click_logout_link()
    print("✓ Step 8: Clicked 'Log out' link")

    # Step 9: Verify login link is visible again
    assert home_page.is_login_link_visible(), "Login link should be visible after logout"
    print("✓ Step 9: Log in link is visible again after logout")

    print("\n All test steps passed successfully!")



