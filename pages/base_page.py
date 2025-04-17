from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        """
        A generic base class for all pages - Handles common browser actions
        :param page: Playwright Page object.
        """
        self.page = page

    def to_locator(self, locator_or_str) -> Locator:
        if isinstance(locator_or_str, str):
            return self.page.locator(locator_or_str)
        return locator_or_str

    def fill(self, locator, value: str):
        """
        Fills a field with the given value.
        :param locator: CSS selector (str) or Locator object
        :param value: text to insert
        """
        self.to_locator(locator).fill(value)

    def click(self, locator):
        """
        Clicks an element.
        :param locator: CSS selector (str) or Locator object
        """
        self.to_locator(locator).click()

    def get_text(self, locator) -> str:
        """
        Gets inner text of an element.
        :param locator: CSS selector (str) or Locator object
        :return: text inside the element
        """
        return self.to_locator(locator).inner_text()

    def wait_for_element(self, locator, timeout: int = 5000, state: str = "visible"):
        """
        Waits for the given element (locator) to reach the desired state.
        :param locator: Can be a string (CSS selector) or Playwright Locator
        :param timeout: Timeout in milliseconds (default 5000)
        :param state: Desired state to wait for. Options: "attached", "detached", "visible", "hidden"
        """
        if isinstance(locator, str):
            self.page.wait_for_selector(locator, timeout=timeout, state=state)
        else:
            locator.wait_for(timeout=timeout, state=state)

    def navigate(self, url: str):
        """
        Navigates to the selected url
        :param url: string
        :return:
        """
        self.page.goto(url)