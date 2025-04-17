from urllib.parse import urlencode
from playwright.sync_api import Page

from pages.base_page import BasePage

class AirbnbReservationPage(BasePage):
    def __init__(self, page: Page):
        """
        Handles actions related to a specific Airbnb listing (reservation page).

        Args:
            page (Page): Playwright Page object.
        """
        super().__init__(page)
        self.page = page
        self.reservation_box = page.locator('[data-plugin-in-point-id="BOOK_IT_SIDEBAR"]')
        self.phone_input = page.locator('input[name="phone"]')

    def go_to_listing(self, room_id: str, check_in: str = None, check_out: str = None, guests: dict = None):
        """
        Navigates directly to the listing page using the given room ID,
        optionally adding check-in, check-out dates and guest parameters.
        Also handles closing any pop-up or modal that appears upon navigation.

        Args:
            room_id (str): The room ID to open.
            check_in (str, optional): Check-in date in YYYY-MM-DD format.
            check_out (str, optional): Check-out date in YYYY-MM-DD format.
            guests (dict, optional): Guests dictionary, e.g., {"adults": 2, "children": 1}.
        """
        base_url = f"https://www.airbnb.com/rooms/{room_id}"

        # Add query parameters if provided
        if check_in and check_out:
            params = {"check_in": check_in, "check_out": check_out}
            if guests:
                params.update(guests)
            full_url = base_url + "?" + urlencode(params)
        else:
            full_url = base_url

        self.navigate(full_url)
        self.page.wait_for_load_state("networkidle")

    def close_popup_if_exists(self):
        """
        Closes a popup/modal if it appears on the page (e.g., login/signup prompts).
        """
        try:
            popup_close_button = self.page.locator('[aria-label="Close"]')
            if popup_close_button.is_visible(timeout=3000):
                popup_close_button.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass  # No popup or not found

    def _safe_get_text(self, selector: str) -> str:
        """
        Safely gets the inner text of an element.
        Returns 'Not Available' if the element is not found or not visible.

        Args:
            selector (str): The CSS selector of the element.

        Returns:
            str: Text content of the element or 'Not Available'.
        """
        try:
            element = self.page.locator(selector)
            if element.is_visible(timeout=3000):
                text = element.inner_text()
                return " ".join(text.split())
            else:
                return "Not Available"
        except Exception:
            return "Not Available"

    def scroll_to_reservation_box(self):
        """
        Scrolls safely to the reservation card section.
        """
        try:
            reservation_section = self.page.locator('[data-plugin-in-point-id="BOOK_IT_SIDEBAR"]')
            reservation_section.first.wait_for(state="attached", timeout=10000)
            reservation_section.first.scroll_into_view_if_needed()
            self.page.wait_for_timeout(1000)

            assert reservation_section.first.is_visible(timeout=5000), "Reservation box is not visible after scroll!"

        except Exception as e:
            raise AssertionError(f"Failed to scroll to reservation section: {e}")

    def save_reservation_details(self) -> dict:
        """
        Scrolls to the reservation box and extracts reservation details like price, guests, dates.
        """
        self.close_popup_if_exists()
        self.scroll_to_reservation_box()
        details = {
            "price_per_night": self._safe_get_text('[data-testid="price-summary"]'),
            "guests": self._safe_get_text('[data-testid="GuestPicker-book_it-trigger"]'),
            "check_in": self._safe_get_text('[data-testid="change-dates-checkIn"]'),
            "check_out": self._safe_get_text('[data-testid="change-dates-checkOut"]')
        }
        return details

    def enter_phone_number(self, phone_number: str):
        """
        Enters the provided phone number into the reservation form.

        Args:
            phone_number (str): The phone number to input.
        """
        self.phone_input.wait_for(state="visible", timeout=5000)
        self.fill(self.phone_input, phone_number)
