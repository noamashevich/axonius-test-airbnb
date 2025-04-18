from playwright.async_api import Page

from pages.base_page import BasePage
from pages.components.calendar_component import DatePickerComponent
from pages.components.guests_component import GuestPickerComponent


class BaseSearchPage(BasePage):
    def __init__(self, page: Page):
        """
        A shared base class for pages that include a search flow (like Airbnb, Booking, etc.)
        :param page: Playwright Page object.
        """
        super().__init__(page)
        self.location_input = page.locator('[data-testid="structured-search-input-field-query"]')
        self.suggestion_by_text = lambda city: page.locator(f'div[role="option"] >> text="{city}"')
        self.search_button = page.locator('[data-testid="structured-search-input-search-button"]')
        self.date_picker = DatePickerComponent(page)
        self.guests_picker = GuestPickerComponent(page)

    def go_to_homepage(self):
        self.navigate("https://www.airbnb.com/")
        # self.page.wait_for_load_state("networkidle")

    def enter_location(self, city: str):
        self.page.wait_for_selector('[data-testid="structured-search-input-field-query"]')  # Extra wait for content to load
        self.page.wait_for_timeout(2000)
        self.click(self.location_input)
        self.fill(self.location_input, city)

        options = self.page.locator('div[role="option"]')
        options.first.wait_for(state="visible", timeout=5000)
        matched = options.filter(has_text=city)

        try:
            matched.first.wait_for(state="visible", timeout=2000)
            matched.first.click()
        except:
            options.first.click()

    def select_dates(self, check_in: str, check_out: str):
        self.date_picker.select_range(check_in, check_out)

    def select_guests(self, **kwargs):
        self.guests_picker.set_guests(**kwargs)

    def search(self):
        self.click(self.search_button)
