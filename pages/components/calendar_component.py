from utils.date_utils import to_airbnb_date_label


class DatePickerComponent:
    def __init__(self, page):
        """
        A component to interact with Airbnb's date picker.
        Args: page: Playwright Page object.
        """
        self.page = page
        self.check_in_button = page.locator('[data-testid="structured-search-input-field-split-dates-0"]')
        self.calendar_root = page.locator('[data-testid="structured-search-input-field-dates-panel"]')
        self.next_month_button = page.locator('button[aria-label="Move forward to switch to the next month."]')
        self.date_cell = lambda date: page.locator(f'button[aria-label*="{date}"]')

    def open(self):
        """
        Opens the calendar by clicking on the check-in button.
        Makes sure the calendar is visible after the click.
        """
        self.check_in_button.wait_for(state="visible", timeout=5000)
        self.check_in_button.click()
        if self.calendar_root.count() == 0:
            self.check_in_button.click()
        assert self.calendar_root.count() > 0, "Calendar did not open after clicking Check in."

    def go_to_month_of(self, date_label):
        """
        Navigates to the month that contains the given date.
        Args: date_label (str): The formatted date string for Airbnb (e.g., 'Friday, April 25, 2025').
        """
        for _ in range(12):
            if self.date_cell(date_label).is_visible():
                return
            self.next_month_button.click()
            self.page.wait_for_timeout(1000)

    def select_range(self, check_in: str, check_out: str):
        """
        Selects a check-in and check-out date in the calendar.
        Args: check_in (str): Check-in date in format 'YYYY-MM-DD'.
        check_out (str): Check-out date in format 'YYYY-MM-DD'.
        """
        self.open()
        check_in_label = to_airbnb_date_label(check_in)
        check_out_label = to_airbnb_date_label(check_out)

        # Wait for date buttons to load
        for _ in range(5):
            count = self.page.locator("button[aria-label]").count()
            if count > 0:
                break
            self.page.wait_for_timeout(500)

        # Select check-in date
        self.go_to_month_of(check_in_label)
        self.date_cell(check_in_label).click()

        # Select check-out date
        self.go_to_month_of(check_out_label)
        self.date_cell(check_out_label).click()