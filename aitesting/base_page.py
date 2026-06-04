"""Base Page class for all page objects."""

from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page):
        """Initialize the base page with a Playwright Page instance.

        Args:
            page: Playwright Page object
        """
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to a given URL.

        Args:
            url: URL to navigate to
        """
        self.page.goto(url)

    def wait_for_element(self, selector: str, timeout: int = 10000) -> None:
        """Wait for an element to be visible.

        Args:
            selector: CSS or XPath selector
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_selector(selector, timeout=timeout)

    def get_element(self, selector: str):
        """Get an element locator.

        Args:
            selector: CSS or XPath selector

        Returns:
            Playwright Locator object
        """
        return self.page.locator(selector)

    def is_element_visible(self, selector: str) -> bool:
        """Check if an element is visible.

        Args:
            selector: CSS or XPath selector

        Returns:
            True if visible, False otherwise
        """
        try:
            element = self.page.locator(selector)
            return element.is_visible()
        except Exception:
            return False

    def get_element_text(self, selector: str) -> str:
        """Get text content of an element.

        Args:
            selector: CSS or XPath selector

        Returns:
            Text content of the element
        """
        return self.page.locator(selector).inner_text()

