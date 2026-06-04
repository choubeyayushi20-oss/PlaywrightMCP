from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.flipkart.com/")

        # close modal if present
        try:
            btn = page.locator("button._2KpZ6l._2doB4z")
            if btn.count() and btn.is_visible():
                btn.click()
        except Exception:
            pass

        page.fill("input[name='q']", "Tshirt")
        page.press("input[name='q']", "Enter")

        page.wait_for_load_state("networkidle")
        # save content and screenshot for inspection
        html = page.content()
        with open(r"C:\Users\sit359\PlaywrightMCP\aitesting\debug_search_result.html", "w", encoding="utf-8") as f:
            f.write(html)
        page.screenshot(path=r"C:\Users\sit359\PlaywrightMCP\aitesting\debug_search_result.png", full_page=True)
        print("Saved debug_search_result.html and .png")
        browser.close()


if __name__ == '__main__':
    run()

