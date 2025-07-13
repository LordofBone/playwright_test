import pytest
from playwright.sync_api import expect

from identifiers import Identifiers


# Test the page loads and that the locators all exist
def test_page_loads(base_navigation):
    # Probably a cleaner way to do this without having to have base_navigation in every test
    browser, page = base_navigation
    for locator_var in Identifiers.Selectors.__dataclass_fields__:
        locator_id = getattr(Identifiers.Selectors, locator_var)
        expect(page.locator(f'#{locator_id}')).to_be_visible()
    browser.close()


# really want to paramaterise this by having the Identifiers class unpack for the params (or have Identifiers in conftest) but doing it this way to save time for this exam
def test_check_mandatory_fields(base_navigation, default_fill, success_message):
    browser, page = base_navigation
    default_fill()
    for locator_var in Identifiers.Selectors.__dataclass_fields__:
        if "mandatory" in locator_var:
            locator_id = getattr(Identifiers.Selectors, locator_var)
            page.locator(f'#{locator_id}').fill("")
            page.locator(f'#{Identifiers.Selectors.button_register}').click()
            expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
            expect(page.locator(f'#{Identifiers.Messages.registered_message}')).not_to_have_text(success_message)


# Check that the password is checked for constraints (0 chars, under 6 chars, and over 20 chars)
@pytest.mark.parametrize("password_fill", ["", "passw", "passwordpasswordpassword"])
def test_password_constraints(base_navigation, default_fill, password_validation_message, password_fill):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.field_password_mandatory}').fill(password_fill)
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_have_text(password_validation_message)


# Checking edge cases for password constraints, exactly 6 chars, and exactly 20 chars
@pytest.mark.parametrize("password_fill", ["passwo", "passwordpasswordpass"])
def test_password_edge_cases(base_navigation, default_fill, success_message, password_fill):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.field_password_mandatory}').fill(password_fill)
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_have_text(success_message)


def test_password_obfuscated(base_navigation):
    browser, page = base_navigation
    page.locator(f'#{Identifiers.Selectors.field_password_mandatory}').fill("password12345")
    expect(page.locator(f'#{Identifiers.Selectors.field_password_mandatory}')).not_to_have_value("password12345")


def test_password_does_not_show_in_results(base_navigation, default_fill):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Results.result_container}')).not_to_contain_text("password123%^&")


# This would be great in future to have default_fill configurable from decorators, like (@pytest.mark.skip_country_fill)
def test_country_left_default(base_navigation, default_fill, success_message):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.dropdown_country_mandatory}').select_option(label="Select a country...")
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).not_to_have_text(success_message)


@pytest.mark.parametrize("number_fill", ["", "12345", "passwordpasswordpassword", "!£$%^&*()_"])
def test_phone_constraints(base_navigation, default_fill, number_fill, success_message):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.field_phone_mandatory}').fill(number_fill)
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).not_to_have_text(success_message)


@pytest.mark.parametrize("number_fill", ["", "12345", "123456789"])
def test_phone_length(base_navigation, default_fill, number_fill, phone_validation_message):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.field_phone_mandatory}').fill(number_fill)
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_have_text(phone_validation_message)


@pytest.mark.parametrize("email_fill", ["", "notanemail", "{}{_)(*&^%$£!}"])
def test_email_validation(base_navigation, default_fill, email_fill, success_message):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.field_email_mandatory}').fill(email_fill)
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).not_to_have_text(success_message)


def test_register_cannot_be_clicked_twice(base_navigation, default_fill, success_message):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    locator = page.locator(f'#{Identifiers.Selectors.button_register}')
    expect(locator).to_be_disabled()


def test_register_double_click(base_navigation, default_fill, success_message):
    browser, page = base_navigation
    default_fill()
    page.locator(f'#{Identifiers.Selectors.button_register}').dblclick()
    expect(page.locator(f'#{Identifiers.Results.result_container}')).to_be_visible()


def test_terms_and_conditions_checkbox_required(base_navigation, default_fill, success_message):
    browser, page = base_navigation
    default_fill()
    expect(page.locator(f'#{Identifiers.Selectors.checkbox_terms_mandatory}')).to_be_checked()
    page.locator(f'#{Identifiers.Selectors.checkbox_terms_mandatory}').check()
    page.locator(f'#{Identifiers.Selectors.checkbox_terms_mandatory}').is_checked()
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_not_have_text(success_message)


# Basic check to make sure the defaults work (putting last as this will only run all the way through if the above tests pass)
def test_happy_path(base_navigation, default_fill, success_message):
    browser, page = base_navigation
    default_fill()
    expect(page.locator(f'#{Identifiers.Selectors.checkbox_terms_mandatory}')).to_be_checked()
    page.locator(f'#{Identifiers.Selectors.checkbox_terms_mandatory}').check()
    page.locator(f'#{Identifiers.Selectors.button_register}').click()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_be_visible()
    expect(page.locator(f'#{Identifiers.Messages.registered_message}')).to_have_text(success_message)
    expect(page.locator(f'#{Identifiers.Results.result_first_name}')).to_have_text("First Name: TestFirstName")
    expect(page.locator(f'#{Identifiers.Results.result_last_name}')).to_have_text("Last Name: TestSecondName")
    expect(page.locator(f'#{Identifiers.Results.result_country}')).to_have_text("Country: New Zealand")
    expect(page.locator(f'#{Identifiers.Results.result_phone}')).to_have_text("Phone Number: 0123456789")
    expect(page.locator(f'#{Identifiers.Results.result_email}')).to_have_text("Email: Test@FakeEmail.net")
