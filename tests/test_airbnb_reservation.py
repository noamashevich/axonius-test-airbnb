"""
Test Case: Airbnb Reservation Flow

This test automates the full booking process on Airbnb:
1. Navigates to the homepage and performs a search.
2. Captures the API search results and identifies the top-rated apartment.
3. Navigates to the selected apartment's listing page.
4. Saves and verifies reservation details.
5. Proceeds to make a reservation and enters a phone number.

Tools Used:
- Playwright (via pytest-playwright plugin)
- Pytest for test organization
"""
import time

import pytest
from utils.logger_utils import print_reservation_details
from pages.search_page import AirbnbPage
from pages.components.api_results_analyzer import ApiResultsAnalyzer
from pages.airbnb_reservation import AirbnbReservationPage

@pytest.mark.parametrize(
    "location, check_in, check_out, guests, phone_number",
    [
        ("Tel Aviv", "2025-05-15", "2025-05-18", {"adults": 2, "children": 1}, "0542341121"),
    ]
)
def test_airbnb_reservation_flow(page, location, check_in, check_out, guests, phone_number):
    """
    Main test that automates the full reservation flow on Airbnb.
    """
    # Arrange
    search_page = AirbnbPage(page)
    search_page.go_to_homepage()

    search_page.enter_location(location)
    search_page.select_dates(check_in, check_out)
    search_page.select_guests(**guests)

    analyzer = ApiResultsAnalyzer(page)
    analyzer.start_capture_api_request()

    page.wait_for_load_state("networkidle")

    # Act
    search_page.search()
    page.wait_for_url(lambda url: "s=" in url)
    page.wait_for_selector('[itemprop="itemListElement"]', timeout=7000)

    # Assert:
    # Step 1: Navigate to homepage and search
    search_page.validate_url_contains({
        "location": location,
        "checkin": check_in,
        "checkout": check_out,
        **guests
    })

    analyzer.fetch_api_results()

    # Step 2: Get the top-rated apartment
    top_rated = analyzer.get_top_rated_from_api()
    assert top_rated is not None, "No top-rated apartment found."
    assert top_rated["id"] is not None, "Top-rated apartment has no ID."

    # Step 3: Go to the listing page directly, including dates and guests
    reservation_page = AirbnbReservationPage(page)
    reservation_page.go_to_listing(
        room_id=top_rated["id"],
        check_in=check_in,
        check_out=check_out,
        guests=guests
    )
    details_before = reservation_page.save_reservation_details()
    print_reservation_details(details_before)
    print(details_before)
    time.sleep(4)
    # reservation_page.click_reserve()
    # reservation_page.validate_reservation_details(details_before)



    #details = reservation_page.save_reservation_details()
    # Step 4: Save reservation details
    # details = reservation_page.save_reservation_details()
    # print_reservation_details(details)

    # reservation_page.click_reserve()
    # reservation_page.validate_reservation_details(details_before)
    # # Step 3: Save and validate reservation details
    # details_before = reservation_page.save_reservation_details()
    # print("Reservation Details (Before Reserve):", details_before)
    # #
    # reservation_page.click_reserve()
    # reservation_page.validate_reservation_details(details_before)
    #
    # # Step 4: Enter a phone number
    # reservation_page.enter_phone_number(phone_number)
