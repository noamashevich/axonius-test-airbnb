from pages.base_page import BasePage
from playwright.sync_api import Page
from pages.components.reservation_box_component import ReservationBoxComponent

class AirbnbReservationPage(BasePage):
    def __init__(self, page: Page):
        """
        Handles actions related to a specific Airbnb listing reservation page.
        """
        super().__init__(page)
        self.page = page
        self.reservation_box_component = ReservationBoxComponent(page)
        self.reserve_button = page.locator('button[data-testid="homes-pdp-cta-btn"]')

    def go_to_listing(self, room_id: str, check_in: str = None, check_out: str = None, guests: dict = None):
        base_url = f"https://www.airbnb.com/rooms/{room_id}"

        params = []
        if check_in:
            params.append(f"check_in={check_in}")
        if check_out:
            params.append(f"check_out={check_out}")
        if guests:
            for guest_type, count in guests.items():
                params.append(f"{guest_type}={count}")

        full_url = base_url + "?" + "&".join(params) if params else base_url

        self.navigate(full_url)
        self.page.wait_for_load_state("networkidle")

    def close_popup_if_exists(self, selector: str):
        ""
        self.page.wait_for_timeout(3000)
        try:
            popup_close = self.page.locator(selector)
            if popup_close.is_visible(timeout=3000):
                popup_close.click()
                self.page.wait_for_timeout(500)
        except:
            pass

    def click_to_reserve_button(self):
        """
        Clicking the reserve button.
        """
        self.page.evaluate(
            """({selector, index}) => document.querySelectorAll(selector)[index].click()""",
            {"selector": '[data-testid="homes-pdp-cta-btn"]', "index": 1}
        )
        self.page.wait_for_timeout(4000)

    def fill_reservation_details(self, countrycode: str, phone_number: str):
        """
        Filling all the fields of the reservation aria
        Countrycode + Phone
        :return:
        """
        country_select = self.page.locator('[data-testid="login-signup-countrycode"]')
        country_select.click()
        self.page.select_option('#country', value=countrycode)
        self.page.wait_for_timeout(5000)
        self.page.fill('input[name="phoneInputphone-login"]', phone_number)
        self.page.wait_for_timeout(5000)

    def get_reservation_data(self):
        """
        Scroll and extract all reservation box data.
        """
        self.close_popup_if_exists('button[aria-label="Close"]')
        self.reservation_box_component.scroll_to_reservation_box()
        return self.reservation_box_component.extract_reservation_box_data()
