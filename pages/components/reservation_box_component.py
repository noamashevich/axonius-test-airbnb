from playwright.sync_api import Page

class ReservationBoxComponent:
    def __init__(self, page: Page):
        self.page = page
        self.reservation_box = self.page.locator('[data-plugin-in-point-id="BOOK_IT_SIDEBAR"]')
        self.reserve_button = self.page.locator('button[data-testid="homes-pdp-cta-btn"]')
        # self.check_in_field = self.page.locator('[data-testid="change-dates-checkIn"]').inner_text()
        # self.check_out_field = self.page.locator('[data-testid="change-dates-checkOut"]').inner_text()
        # self.guests_field = self.page.locator('div#GuestPicker-book_it-trigger span._j1kt73').inner_text()
        # self.total_price_field = self.page.locator('[data-testid="change-dates-checkOut"]').inner_text()
        # self.price_per_night_field = self.page.locator('[data-testid="change-dates-checkOut"]').inner_text()

    def click_reserve(self):
        self.reserve_button.wait_for(state="visible", timeout=5000)
        self.reserve_button.click(force=True)

    def get_check_in_date(self) -> str:
        return self.check_in_field.inner_text()

    def get_check_out_date(self) -> str:
        return self.check_out_field.inner_text()

    def get_guest_info(self) -> str:
        return self.guest_field.inner_text()

    def return_reservation_details(self) -> dict:
        return {
            "price_per_night": self.price_per_night_field,
            "total_price": self.total_price_field,
            "guests": self.guests_field,
            "check_in": self.check_in_field,
            "check_out": self.check_out_field,
        }

    def print_reservation_details(details: dict):
        """
        Prints reservation details in a clear and clean format.
        Args: details (dict): Dictionary containing reservation details.
        """
        print("\nReservation Details:")
        print("-" * 50)
        for key, value in details.items():
            key_pretty = key.replace("_", " ").capitalize()

            if not value or value == "Not Found":
                value = "Not Available"

            if isinstance(value, str):
                value = " ".join(value.split())

            print(f"{key_pretty:<15}: {value}")
        print("-" * 50 + "\n")
