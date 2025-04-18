import re

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

        self.page.wait_for_timeout(3000)  # Extra wait for box content to load
        try:
            popup_close = self.page.locator('button[aria-label="Close"]')
            if popup_close.is_visible(timeout=3000):
                popup_close.click()
                self.page.wait_for_timeout(500)
        except:
            pass  # Ignore errors if no popup

    def scroll_to_reservation_box(self):
        """
        Aggressively scrolls down until the reservation box becomes visible.
        Scrolls deeply to ensure even the total price is loaded.
        """
        self.close_popup_if_exists()
        try:
            for _ in range(100):  # Try scrolling 100 times
                if self.reservation_box.is_visible(timeout=4000):
                    print("Reservation box is now visible!")
                    # self.page.wait_for_timeout(2000)  # Extra wait for box content to load
                    return

                self.page.mouse.wheel(0, 10000)  # Scroll much deeper
                self.page.wait_for_timeout(1500)  # Wait longer after each scroll

            raise AssertionError("Could not find the reservation box after scrolling.")

        except Exception as e:
            raise AssertionError(f"Failed to scroll to reservation box: {e}")

    def get_total_price(self) -> str:
        """
        Fetches only the 'Total Price' from the reservation box.
        Returns:
            str: Total price text, or 'Not Available' if not found.
        """
        try:
            total_price_locator = self.page.locator('div._1avmy66 span._1qs94rc span._j1kt73')
            total_price_locator.wait_for(state="visible", timeout=5000)

            price_text = total_price_locator.inner_text()
            return " ".join(price_text.split())

        except Exception as e:
            print(f"Failed to fetch total price: {e}")
            return "Not Available"

    def extract_reservation_box_data_with_scroll(self) -> dict:
        """
        Scrolls to the reservation box and extracts reservation details using pure CSS selectors.
        Returns: dict: Reservation data including price per night, total price, guests, check-in, check-out.
        """
        try:
            self.close_popup_if_exists()
            self.scroll_to_reservation_box()

            selectors = {
                "price_per_night": 'span._hb913q',
                "guests": 'div#GuestPicker-book_it-trigger span._j1kt73',
                "check_in": '[data-testid="change-dates-checkIn"]',
                "check_out": '[data-testid="change-dates-checkOut"]'
            }

            data = {}

            def get_total_price_element(page):
                # Try to find the second element with _j1kt73
                elements = page.locator('span._j1kt73')
                count = elements.count()

                if count >= 2:
                    # If second exists, return it
                    return elements.nth(1).inner_text()
                else:
                    # Else, fallback to the first _1vk118j element
                    fallback = page.locator('div._1vk118j').first.inner_text()
                    return fallback

            def extract_price_only(text: str) -> str:
                """
                Extracts the first price (with currency symbol) from a text.
                Supports multiple currencies: ₪, $, €, £, etc.
                """
                match = re.search(r'[₪$€£]\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
                if match:
                    return match.group().replace(' ', '')
                return "Not Available"

            for key, selector in selectors.items():
                locator = self.page.locator(selector)
                try:
                    locator.scroll_into_view_if_needed()
                    locator.wait_for(state="visible", timeout=8000)

                    text = locator.inner_text()
                    # Cleaning &nbsp;
                    clean_text = " ".join(text.replace("\xa0", " ").split())
                    data[key] = clean_text

                except Exception as e:
                    print(f"Failed to extract {key}: {e}")
                    data[key] = "Not Available"

            total_price = get_total_price_element(self.page)
            price = extract_price_only(total_price)
            data["total_price"] = price
            return data

        except Exception as e:
            raise AssertionError(f"Failed to extract reservation box data: {e}")

    def click_to_reserve_button(self):
        """
        Clicking the reserve button
        :return:
        """
        self.page.evaluate(
            """({selector, index}) => document.querySelectorAll(selector)[index].click()""",
            {"selector": '[data-testid="homes-pdp-cta-btn"]', "index": 1}
        )

        self.page.wait_for_timeout(4000)

    def fill_reservation_details(self):
        country_select = self.page.locator('[data-testid="login-signup-countrycode"]')
        country_select.click()
        self.page.select_option('#country', value='93AF')
        self.page.wait_for_timeout(5000)

        self.page.fill('input[name="phoneInputphone-login"]', '0542341121')
        self.page.wait_for_timeout(5000)

