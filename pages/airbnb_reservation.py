from pages.base_page import BasePage
from playwright.sync_api import Page
import os

class AirbnbReservationPage(BasePage):
    def __init__(self, page: Page):
        """
        Handles actions related to a specific Airbnb listing reservation page.
        """
        super().__init__(page)
        self.page = page
        self.reservation_box = page.locator('[data-plugin-in-point-id="BOOK_IT_SIDEBAR"]')
        self.reserve_button = page.locator('button[data-testid="homes-pdp-cta-btn"]')

    def go_to_listing(self, room_id: str, check_in: str = None, check_out: str = None, guests: dict = None):
        """
        Navigates to the Airbnb listing page with optional check-in, check-out, and guests parameters.

        Args:
            room_id (str): The room ID of the listing.
            check_in (str, optional): Check-in date in format YYYY-MM-DD.
            check_out (str, optional): Check-out date in format YYYY-MM-DD.
            guests (dict, optional): Dictionary of guests, e.g., {"adults": 2, "children": 1}.
        """
        base_url = f"https://www.airbnb.com/rooms/{room_id}"

        # Add query params if provided
        params = []
        if check_in:
            params.append(f"check_in={check_in}")
        if check_out:
            params.append(f"check_out={check_out}")
        if guests:
            for guest_type, count in guests.items():
                params.append(f"{guest_type}={count}")

        if params:
            full_url = base_url + "?" + "&".join(params)
        else:
            full_url = base_url

        self.navigate(full_url)
        self.page.wait_for_load_state("networkidle")

    def close_popup_if_exists(self):
        """
        Tries to close any popup (like login/signup) that appears.
        """
        try:
            popup_close = self.page.locator('[aria-label="Close"]')
            if popup_close.is_visible(timeout=3000):
                popup_close.click()
                self.page.wait_for_timeout(500)
        except:
            pass  # Ignore errors if no popup

    def scroll_to_reservation_box(self):
        """
        Gradually scrolls down until the reservation box becomes visible.
        Takes a screenshot after scrolling for debugging.
        """
        self.close_popup_if_exists()
        self.page.wait_for_timeout(2000)

        try:
            for _ in range(20):  # Try scrolling up to 20 times
                if self.reservation_box.is_visible(timeout=1000):
                    print("✅ Reservation box is now visible!")
                    # Extra wait to ensure box contents fully load
                    self.page.wait_for_timeout(2000)
                    self.page.screenshot(path="after_scroll.png", full_page=True)
                    return

                self.page.mouse.wheel(0, 600)  # Scroll down
                self.page.wait_for_timeout(500)

            raise AssertionError("❌ Could not find the reservation box after scrolling.")
        except Exception as e:
            raise AssertionError(f"❌ Failed to scroll to reservation box: {e}")

    def _safe_get_text(self, selector: str) -> str:
        """
        Safely gets text from a selector, returns 'Not Available' if not found.
        """
        try:
            element = self.page.locator(selector)
            if element.is_visible(timeout=3000):
                text = element.inner_text()
                return " ".join(text.split())  # Normalize spaces
            else:
                return "Not Available"
        except Exception:
            return "Not Available"

    def save_reservation_details(self) -> dict:
        """
        After navigating and scrolling, extract reservation details like price, guests, check-in, and check-out.
        """
        # Close any popups if exist
        self.close_popup_if_exists()

        # Scroll to the reservation section
        self.scroll_to_reservation_box()

        try:
            details = {}

            # Wait for the reservation box to appear
            self.page.locator('[data-plugin-in-point-id="BOOK_IT_SIDEBAR"]').wait_for(state="visible", timeout=10000)

            # Extract values carefully
            details['price_per_night'] = self._safe_get_text('div._zo8nmn span._hb913q')  # מחיר ללילה
            details['total_price'] = self._safe_get_text('div._1avmy66 span._j1kt73')  # מחיר כולל

            details['guests'] = self._safe_get_text('div#GuestPicker-book_it-trigger span._j1kt73')  # כמות אורחים
            details['check_in'] = self._safe_get_text('[data-testid="change-dates-checkIn"]')
            details['check_out'] = self._safe_get_text('[data-testid="change-dates-checkOut"]')

            return details

        except Exception as e:
            raise AssertionError(f"Failed to extract reservation details: {e}")

    def print_reservation_details(self, details: dict):
        """
        Pretty-prints the reservation details.
        """
        print("\nReservation Details:")
        print("-" * 50)
        for key, value in details.items():
            key_pretty = key.replace("_", " ").capitalize()
            if not value or value == "Not Available":
                value = "Not Available"
            if isinstance(value, str):
                value = " ".join(value.split())
            print(f"{key_pretty:<20}: {value}")
        print("-" * 50)
