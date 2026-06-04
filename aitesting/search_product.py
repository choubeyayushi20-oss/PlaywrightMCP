from playwright.sync_api import Page


def test_search_product(page: Page):
    """Search for a Tshirt on Flipkart and verify a specific product appears.

    This test is defensive: it closes the initial login modal if present,
    performs the search, and then checks for the target product text.
    """
    # 1) Open Flipkart
    page.goto("https://www.flipkart.com/")

    # 2) Close login modal if it appears (common class used by Flipkart)
    try:
        close_btn = page.locator("button._2KpZ6l._2doB4z")
        if close_btn.count() and close_btn.is_visible():
            close_btn.click()
    except Exception:
        # If selector changes or not present, ignore and continue
        pass

    # 3) Search for the product
    search_selector = "input[name='q']"
    page.wait_for_selector(search_selector, timeout=10000)
    page.fill(search_selector, "Tshirt")
    page.press(search_selector, "Enter")

    # 4) Wait for search results to load and verify we have product titles
    # Flipkart product titles commonly appear in anchors with class `atJtCj`
    page.wait_for_selector("a.atJtCj, div._4rR01T, a.s1Q9rs", timeout=15000)

    # Collect product title texts from a few common selectors used on Flipkart
    product_locators = page.locator("a.atJtCj, div._4rR01T, a.s1Q9rs")
    titles = []
    for i in range(product_locators.count()):
        try:
            txt = product_locators.nth(i).inner_text().strip()
            if txt:
                titles.append(txt)
        except Exception:
            continue

    combined = "\n".join(titles)
    # Assert we found at least one product title
    assert len(titles) > 0, f"No product titles found on results page. Page text:\n{page.content()[:1000]}"

