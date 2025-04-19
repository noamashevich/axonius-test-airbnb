import re
from playwright.sync_api import Page

class ReservationBoxComponent:
    """
    Represents the Reservation Box component on an Airbnb listing page.
    Handles scrolling to the reservation box and extracting its displayed details.
    """

    def __init__(self, page: Page):
        """
        Initializes the ReservationBoxComponent.
        Args: page (Page): Playwright Page object controlling the browser.
        """
        self.page = page
        self.reservation_box = page.locator('[data-plugin-in-point-id="BOOK_IT_SIDEBAR"]')

    def scroll_to_reservation_box(self):
        """
        Scrolls aggressively until the reservation box becomes visible on the page.
        Raises: AssertionError: If the reservation box is not found after multiple scroll attempts.
        """
        try:
            for _ in range(50):  # Limit scroll attempts to avoid infinite loops
                if self.reservation_box.is_visible(timeout=1500):
                    print("Reservation box is now visible!")
                    return
                self.page.mouse.wheel(0, 1000)
                self.page.wait_for_timeout(1500)

            raise AssertionError("Could not find the reservation box after scrolling.")
        except Exception as e:
            raise AssertionError(f"Failed to scroll to reservation box: {e}")

    def extract_reservation_box_data(self) -> dict:
        """
        Extracts important reservation details from the reservation box:
        - Price per night
        - Total price
        - Number of guests
        - Check-in date
        - Check-out dat
        Returns:
            dict: A dictionary containing the extracted reservation data.
                  Example:
                  {
                      "price_per_night": "₪817",
                      "total_price": "₪2,451",
                      "guests": "3 guests",
                      "check_in": "5/15/2025",
                      "check_out": "5/18/2025"
                  }
        """
        selectors = {
            "price_per_night": 'span._hb913q',
            "guests": 'div#GuestPicker-book_it-trigger span._j1kt73',
            "check_in": '[data-testid="change-dates-checkIn"]',
            "check_out": '[data-testid="change-dates-checkOut"]'
        }
        data = {}

        def get_total_price_element(page: Page) -> str:
            """
            Finds the total price element by attempting to locate the second matching price element.
            Fallbacks to an alternative selector if needed.
            Args: page (Page): Playwright Page object.
            Returns: str: The total price text.
            """
            elements = page.locator('span._j1kt73')
            count = elements.count()
            if count >= 2:
                return elements.nth(1).inner_text()
            else:
                fallback = page.locator('div._1vk118j').first.inner_text()
                return fallback

        def extract_price_only(text: str) -> str:
            """
            Extracts the first currency price found within a text string.
            Supports multiple currencies like ₪, $, €, £.
            Args: text (str): Text containing the price.
            Returns: str: Clean price string, or "Not Available" if extraction fails.
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
                clean_text = " ".join(text.replace("\xa0", " ").split())
                data[key] = clean_text
            except Exception as e:
                print(f"Failed to extract {key}: {e}")
                data[key] = "Not Available"

        total_price = get_total_price_element(self.page)
        data["total_price"] = extract_price_only(total_price)

        return data
