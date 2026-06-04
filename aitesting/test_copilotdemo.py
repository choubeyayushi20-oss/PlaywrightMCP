
from playwright.sync_api import Page


def test_login(page:Page):
    # Navigate to Google and verify the page title
    page.goto("https://www.google.com/")
    assert page.title() == "Google"

    # Reuse the locator for clarity and efficiency
    search = page.locator("//textarea[@name='q']")
    search.fill("Playwright")
    search.press("Enter")
    page.wait_for_selector("//h3[contains(text(), 'Playwright')]")

    # Wait for search results that contain the query text instead of an arbitrary timeout
    page.wait_for_selector("text=Playwright", timeout=10000)
    page.close()
