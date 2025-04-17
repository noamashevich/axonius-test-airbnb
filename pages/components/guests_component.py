class GuestPickerComponent:
    def __init__(self, page):
        """
        Manages the selection of the number of guests
        :param page: Playwright Page object.
        """
        self.page = page
        self.guest_button = page.locator('[data-testid="structured-search-input-field-guests-button"]')
        self.controls = {
            "adults": page.locator('[data-testid="stepper-adults-increase-button"]'),
            "children": page.locator('[data-testid="stepper-children-increase-button"]'),
            "infants": page.locator('[data-testid="stepper-infants-increase-button"]'),
            "pets": page.locator('[data-testid="stepper-pets-increase-button"]')
        }

    def open(self):
        self.guest_button.wait_for(state="visible", timeout=5000)
        self.guest_button.click()
        self.page.wait_for_timeout(500)

    def set_guests(self, is_service_dog=False, **kwargs):
        self.open()
        for category, amount in kwargs.items():
            if category == "is_service_dog":
                continue
            if category == "pets" and is_service_dog:
                print("Skipping pets selection due to service dog.")
                continue
            if category in self.controls:
                for _ in range(amount):
                    self.controls[category].click()