"""Login Page Object Model for DemoBlaze."""

from playwright.sync_api import Page
from .base_page import BasePage


class LoginPage(BasePage):
    """Login page object for DemoBlaze application."""

    # Locators for Login page
    LOGIN_LINK = "//a[contains(text(), 'Log in')]"
    USERNAME_FIELD = "//input[@id='loginusername']"
    PASSWORD_FIELD = "//input[@id='loginpassword']"
    LOGIN_BUTTON = "//button[contains(text(), 'Log in')]"
    LOGIN_MODAL = "//div[@id='logInModal']"

    def __init__(self, page: Page):
        """Initialize the Login page.

        Args:
            page: Playwright Page object
        """
        super().__init__(page)

    def click_login_link(self) -> None:
        """Click on the Login link in the navigation bar."""
        self.page.locator(self.LOGIN_LINK).click()
        # Wait for the login modal to appear
        self.page.wait_for_selector(self.LOGIN_MODAL, timeout=10000)

    def enter_username(self, username: str) -> None:
        """Enter username in the username field.

        Args:
            username: Username to enter
        """
        username_input = self.page.locator(self.USERNAME_FIELD)
        username_input.fill(username)

    def enter_password(self, password: str) -> None:
        """Enter password in the password field.

        Args:
            password: Password to enter
        """
        password_input = self.page.locator(self.PASSWORD_FIELD)
        password_input.fill(password)

    def click_login_button(self) -> None:
        """Click the Login button to submit the login form."""
        self.page.locator(self.LOGIN_BUTTON).click()

    def login(self, username: str, password: str) -> None:
        """Perform complete login flow.

        Args:
            username: Username to login
            password: Password to login
        """
        self.click_login_link()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        # Wait for the modal to close (logout link should appear)
        self.page.wait_for_selector("//a[contains(text(), 'Log out')]", timeout=10000)




