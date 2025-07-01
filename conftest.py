from identifiers import Identifiers
import pytest
from playwright.sync_api import sync_playwright, Playwright, expect

# Keeping response messages here to be tidy
@pytest.fixture(scope="session", autouse=True)
def success_message():
    return "Successfully registered the following information"

@pytest.fixture(scope="session", autouse=True)
def password_validation_message():
    return "The password should contain between [6,20] characters!"

@pytest.fixture(scope="session", autouse=True)
def phone_validation_message():
    return "The phone number should contain at least 10 characters!"

@pytest.fixture
def runner():
    with sync_playwright() as playwright:
        # Believe that this will destroy the playwright session after each test
        yield playwright

# Using examples from https://playwright.dev/python/docs/api/class-playwright to build around
@pytest.fixture
def base_navigation(runner: Playwright):
    chromium = runner.chromium
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(Identifiers.URL.base)
    return browser, page

# Probably a better way to do this, using a fixture wrapped around a func so that it is callable during test time
@pytest.fixture
def default_fill(runner: Playwright, base_navigation):
    def fill():
        browser, page = base_navigation
        page.locator(f'#{Identifiers.Selectors.field_first_name}').fill("TestFirstName")
        page.locator(f'#{Identifiers.Selectors.field_last_name_mandatory}').fill("TestSecondName")
        page.locator(f'#{Identifiers.Selectors.dropdown_country_mandatory}').select_option(label="New Zealand")
        page.locator(f'#{Identifiers.Selectors.field_phone_mandatory}').fill("0123456789")
        page.locator(f'#{Identifiers.Selectors.field_email_mandatory}').fill("Test@FakeEmail.net")
        page.locator(f'#{Identifiers.Selectors.field_password_mandatory}').fill("password123%^&")
    return fill