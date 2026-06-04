"""Home Page Object Model for DemoBlaze."""

from playwright.sync_api import Page
from .base_page import BasePage


class HomePage(BasePage):
    """Home page object for DemoBlaze application."""

    # Locators for Home page
    LOGOUT_LINK = "//a[contains(text(), 'Log out')]"
    LOGIN_LINK = "//a[contains(text(), 'Log in')]"
    WELCOME_TEXT = "//*[contains(text(), 'Welcome')]"

    def __init__(self, page: Page):
        """Initialize the Home page.

        Args:
            page: Playwright Page object
        """
        super().__init__(page)

    def is_logout_link_visible(self) -> bool:
        """Check if the logout link is visible.

        Returns:
            True if logout link is visible, False otherwise
        """
        return self.is_element_visible(self.LOGOUT_LINK)

    def is_login_link_visible(self) -> bool:
        """Check if the login link is visible.

        Returns:
            True if login link is visible, False otherwise
        """
        return self.is_element_visible(self.LOGIN_LINK)

    def get_welcome_text(self) -> str:
        """Get the welcome text displayed at the top right.

        Returns:
            Welcome text content
        """
        try:
            return self.get_element_text(self.WELCOME_TEXT)
        except Exception:
            return ""

    def click_logout_link(self) -> None:
        """Click on the Logout link."""
        self.page.locator(self.LOGOUT_LINK).click()
        # Wait for login link to appear after logout
        self.page.wait_for_selector("//a[contains(text(), 'Log in')]", timeout=10000)

    def verify_welcome_message(self, username: str) -> bool:
        """Verify that the welcome message contains the expected username.

        Args:
            username: Expected username in the welcome message

        Returns:
            True if welcome message contains the username, False otherwise
        """
        welcome_text = self.get_welcome_text()
        return username in welcome_text





