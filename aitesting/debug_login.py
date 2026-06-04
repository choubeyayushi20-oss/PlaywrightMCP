"""Debug script to inspect the page after login and find correct selectors."""

import sys
sys.path.insert(0, 'C:\\Users\\sit359\\PlaywrightMCP')

from playwright.sync_api import sync_playwright
from aitesting.login_page import LoginPage
from aitesting.home_page import HomePage


def debug_after_login():
    """Debug script to inspect page elements after login."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to DemoBlaze
        page.goto("https://www.demoblaze.com/")
        print("✓ Navigated to DemoBlaze")

        # Initialize page objects
        login_page = LoginPage(page)

        # Login
        login_page.click_login_link()
        login_page.enter_username("pavanol")
        login_page.enter_password("test@123")
        login_page.click_login_button()
        page.wait_for_selector("//a[contains(text(), 'Log out')]", timeout=10000)
        print("✓ Login successful")

        # Debug: Print all text content on the page
        page_text = page.content()
        print("\n=== Page HTML (first 2000 chars) ===")
        print(page_text[:2000])

        # Try different selectors to find the welcome text
        selectors_to_try = [
            "//span[@id='nameofuser']",
            "//span[contains(text(), 'Welcome')]",
            "//span[contains(text(), 'pavanol')]",
            "//div[contains(text(), 'Welcome')]",
            "//*[contains(text(), 'Welcome')]",
            "//*[contains(text(), 'pavanol')]",
        ]

        print("\n=== Testing selectors for welcome text ===")
        for selector in selectors_to_try:
            try:
                element = page.locator(selector)
                if element.count() > 0:
                    text = element.inner_text()
                    is_visible = element.is_visible()
                    print(f"✓ Found with '{selector}':")
                    print(f"  Text: '{text}'")
                    print(f"  Visible: {is_visible}")
                else:
                    print(f"✗ No elements found for '{selector}'")
            except Exception as e:
                print(f"✗ Error with '{selector}': {e}")

        # Let's also check the logout link
        print("\n=== Logout link info ===")
        logout_selector = "//a[contains(text(), 'Log out')]"
        logout_element = page.locator(logout_selector)
        print(f"Logout link visible: {logout_element.is_visible()}")
        print(f"Logout link text: '{logout_element.inner_text()}'")

        # Keep browser open for inspection
        print("\n✓ Debug complete. Browser will stay open for inspection.")
        input("Press Enter to close browser...")

        browser.close()


if __name__ == "__main__":
    debug_after_login()


