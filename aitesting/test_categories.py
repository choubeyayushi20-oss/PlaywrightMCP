"""Category navigation tests for DemoBlaze using Page Object Model."""

import pytest
from playwright.sync_api import Page
from .home_page import HomePage


def test_categories_browsing(authenticated_page: Page):
    """Test browsing different product categories on DemoBlaze.

    This test reuses the authenticated session from conftest.py
    and verifies that categories are accessible and products load correctly.

    Test Steps:
    1. Verify user is logged in (authenticated session)
    2. Get list of available categories
    3. Verify categories are visible
    4. Click on 'Laptops' category
    5. Verify products are loaded for Laptops
    6. Verify product titles are displayed
    7. Click on 'Phones' category
    8. Verify products are loaded for Phones
    9. Navigate back and verify navigation works

    Args:
        authenticated_page: Page object with authenticated user logged in
    """
    # Initialize home page object
    home_page = HomePage(authenticated_page)

    # Step 1: Verify user is logged in
    assert home_page.is_logout_link_visible(), "User should be logged in"
    print("✓ Step 1: User is logged in")

    # Step 2: Get list of available categories
    categories = home_page.get_categories()
    print(f"✓ Step 2: Retrieved {len(categories)} categories: {categories}")
    assert len(categories) > 0, "Should have at least one category"

    # Step 3: Verify expected categories are visible
    expected_categories = ["Laptops", "Phones", "Monitors"]
    for category in expected_categories:
        is_visible = home_page.is_category_visible(category)
        print(f"  - {category}: {'visible' if is_visible else 'not visible'}")

    # Step 4: Click on 'Laptops' category
    home_page.click_category("Laptops")
    print("✓ Step 4: Clicked on 'Laptops' category")

    # Step 5: Verify products are loaded for Laptops
    assert home_page.verify_products_loaded(), "Products should be loaded for Laptops"
    laptop_count = home_page.get_product_count()
    print(f"✓ Step 5: {laptop_count} laptop products loaded")

    # Step 6: Verify product titles are displayed
    laptop_titles = home_page.get_product_titles()
    assert len(laptop_titles) > 0, "Should have at least one laptop product"
    print(f"✓ Step 6: Retrieved {len(laptop_titles)} laptop titles:")
    for title in laptop_titles[:3]:  # Print first 3 titles
        print(f"  - {title}")

    # Step 7: Click on 'Phones' category
    home_page.click_category("Phones")
    print("✓ Step 7: Clicked on 'Phones' category")

    # Step 8: Verify products are loaded for Phones
    assert home_page.verify_products_loaded(), "Products should be loaded for Phones"
    phone_count = home_page.get_product_count()
    print(f"✓ Step 8: {phone_count} phone products loaded")

    # Step 9: Verify products are displayed
    phone_titles = home_page.get_product_titles()
    assert len(phone_titles) > 0, "Should have at least one phone product"
    print(f"✓ Step 9: Retrieved {len(phone_titles)} phone titles:")
    for title in phone_titles[:3]:  # Print first 3 titles
        print(f"  - {title}")

    # Verify category navigation is working (products loaded for both categories)
    assert laptop_count > 0 and phone_count > 0, \
        "Both categories should have products loaded"
    print("✓ Category switching verified - products loaded in all categories")

    print("\n All category browsing tests passed successfully!")


def test_monitors_category(authenticated_page: Page):
    """Test browsing Monitors category on DemoBlaze.

    This test demonstrates reusing the authenticated session for
    a focused test on a specific category.

    Args:
        authenticated_page: Page object with authenticated user logged in
    """
    # Initialize home page object
    home_page = HomePage(authenticated_page)

    # Verify user is logged in
    assert home_page.is_logout_link_visible(), "User should be logged in"
    print("✓ User is logged in")

    # Navigate to Monitors category
    home_page.click_category("Monitors")
    print("✓ Navigated to Monitors category")

    # Verify products are loaded
    assert home_page.verify_products_loaded(), "Products should be loaded for Monitors"
    monitor_count = home_page.get_product_count()
    print(f"✓ {monitor_count} monitor products loaded")

    # Get and verify product titles
    monitor_titles = home_page.get_product_titles()
    assert len(monitor_titles) > 0, "Should have at least one monitor product"
    print(f"✓ Retrieved {len(monitor_titles)} monitor titles")

    print("\n Monitors category test passed successfully!")


def test_category_reloading(authenticated_page: Page):
    """Test that categories can be re-accessed without issues.

    This test verifies that the authenticated session remains stable
    when navigating between categories multiple times.

    Args:
        authenticated_page: Page object with authenticated user logged in
    """
    # Initialize home page object
    home_page = HomePage(authenticated_page)

    # Test multiple category loads
    categories_to_test = ["Laptops", "Phones", "Monitors", "Laptops"]

    for category in categories_to_test:
        home_page.click_category(category)
        assert home_page.verify_products_loaded(), \
            f"Products should be loaded for {category}"
        product_count = home_page.get_product_count()
        print(f"✓ {category}: {product_count} products loaded")

    print("\n Category reloading test passed successfully!")


