from dataclasses import dataclass


# Probably wrong use of dataclasses here, but it works for the time, being; with more time would move this to conftest as a nice fixture
# Mainly did this to have a clean location for all locators
@dataclass
class Identifiers:
    @dataclass
    class URL:
        base: str = "https://qa-practice.netlify.app/bugs-form"

    @dataclass
    class Selectors:
        field_first_name: str = "firstName"
        field_last_name_mandatory: str = "lastName"
        field_phone_mandatory: str = "phone"
        dropdown_country_mandatory: str = "countries_dropdown_menu"
        field_email_mandatory: str = "emailAddress"
        field_password_mandatory: str = "password"
        checkbox_terms_mandatory: str = "exampleCheck1"
        button_register: str = "registerBtn"

    @dataclass
    class Messages:
        registered_message: str = "message"

    @dataclass
    class Results:
        result_container: str = "results-section"
        result_first_name: str = "resultFn"
        result_last_name: str = "resultLn"
        result_phone: str = "resultPhone"
        result_country: str = "country"
        result_email: str = "resultEmail"
