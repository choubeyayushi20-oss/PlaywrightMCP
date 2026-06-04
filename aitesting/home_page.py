"""Home Page Object Model for DemoBlaze."""

from playwright.sync_api import Page
from .base_page import BasePage


class HomePage(BasePage):
    """Home page object for DemoBlaze application."""

    # Locators for Home page
    LOGOUT_LINK = "//a[contains(text(), 'Log out')]"
    LOGIN_LINK = "//a[contains(text(), 'Log in')]"
    WELCOME_TEXT = "//*[contains(text(), 'Welcome')]"

    # Locators for Categories
    CATEGORY_LIST = "//div[@class='list-group']//a"
    CATEGORY_ITEM = "//a[@data-category='{category}']"
    PRODUCT_LIST = "//div[contains(@class, 'col-lg')]"
    PRODUCT_TITLE = "//a[contains(@class, 'hrefch')]"
    CATEGORY_LINK_BY_TEXT = "//a[contains(text(), '{category}')]"

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

    def get_categories(self) -> list:
        """Get list of all available categories.

        Returns:
            List of category names
        """
        try:
            category_elements = self.page.locator(self.CATEGORY_LIST)
            categories = []
            for i in range(category_elements.count()):
                try:
                    text = category_elements.nth(i).inner_text().strip()
                    if text:
                        categories.append(text)
                except Exception:
                    continue
            return categories
        except Exception:
            return []

    def click_category(self, category_name: str) -> None:
        """Click on a category by name.

        Args:
            category_name: Name of the category to click (e.g., 'Laptops', 'Phones')
        """
        category_selector = self.CATEGORY_LINK_BY_TEXT.format(category=category_name)
        self.page.locator(category_selector).click()
        # Wait for products to load by waiting for product titles to appear
        self.page.wait_for_selector(self.PRODUCT_TITLE, timeout=10000)

    def get_product_count(self) -> int:
        """Get the number of products displayed on the page.

        Returns:
            Number of products
        """
        try:
            # Count product titles which is more reliable than counting containers
            product_elements = self.page.locator(self.PRODUCT_TITLE)
            return product_elements.count()
        except Exception:
            return 0

    def get_product_titles(self) -> list:
        """Get list of product titles on the current page.

        Returns:
            List of product titles
        """
        try:
            product_elements = self.page.locator(self.PRODUCT_TITLE)
            titles = []
            for i in range(product_elements.count()):
                try:
                    text = product_elements.nth(i).inner_text().strip()
                    if text:
                        titles.append(text)
                except Exception:
                    continue
            return titles
        except Exception:
            return []

    def is_category_visible(self, category_name: str) -> bool:
        """Check if a specific category is visible.

        Args:
            category_name: Name of the category

        Returns:
            True if category is visible, False otherwise
        """
        category_selector = self.CATEGORY_LINK_BY_TEXT.format(category=category_name)
        return self.is_element_visible(category_selector)

    def verify_products_loaded(self) -> bool:
        """Verify that products are loaded on the page.

        Returns:
            True if at least one product is visible, False otherwise
        """
        try:
            return self.get_product_count() > 0
        except Exception:
            return False





