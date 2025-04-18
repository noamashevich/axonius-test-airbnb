import pytest
from pages.components.reservation_box_component import ReservationBoxComponent
from pages.search_page import AirbnbPage
from pages.components.api_results_analyzer import ApiResultsAnalyzer
from pages.airbnb_reservation import AirbnbReservationPage
from utils.date_utils import validate_date_logic
from utils.logger_utils import print_reservation_details


@pytest.mark.parametrize(
    "location, check_in, check_out, guests",
    [
        ("Tel Aviv", "2025-05-15", "2025-05-18", {"adults": 2, "children": 1}),
    ]
)
def test_airbnb_reservation_flow(page, location, check_in, check_out, guests):
    """
    End-to-end test for Airbnb flow:
    1. Search apartments
    2. Analyze API results
    3. Open the top-rated apartment
    4. Save reservation details
    5. Validate consistency
    """
    search_page = AirbnbPage(page)
    analyzer = ApiResultsAnalyzer(page)

    # Step 1: Search for apartments
    search_page.go_to_homepage()
    analyzer.start_capture_api_request()

    search_page.enter_location(location)
    validate_date_logic(check_in, check_out)
    search_page.select_dates(check_in, check_out)
    search_page.select_guests(**guests)

    # Act
    search_page.search()
    page.wait_for_url(lambda url: "s=" in url)
    page.wait_for_selector('[itemprop="itemListElement"]', timeout=7000)

    # Assert:
    # Validate URL parameters
    search_page.validate_url_contains({
        "location": location,
        "checkin": check_in,
        "checkout": check_out,
        **guests
    })

    analyzer.fetch_api_results()

    # Step 2: Pick top-rated apartment
    top_rated = analyzer.get_top_rated_from_api()
    assert top_rated is not None, "No top-rated apartment found."
    assert top_rated["id"] is not None, "Top-rated apartment has no ID."

    # Reservation box object
    reservation_page = AirbnbReservationPage(page)

    # Step 3: Go to the listing page
    reservation_page.go_to_listing(top_rated["id"], check_in, check_out, guests)

    # Step 4: Save reservation details
    details = reservation_page.extract_reservation_box_data_with_scroll()
    print_reservation_details(details)

    # Clicking the reservation button
    reservation_page.click_to_reserve_button()
    reservation_page.fill_reservation_details()


    # Validate URL AGAIN
    # search_page.validate_url_contains({
    #     "checkin": check_in,
    #     "checkout": check_out,
    #     **guests
    # })

    # Enter phone number
    #
    # # Step 5: Reserve the listing
    # reservation_page.click_reserve_button()
    #



    # # Step 6: Basic validation
    # assert details.get("check_in") != "Not Available", "Check-in date missing!"
    # assert details.get("check_out") != "Not Available", "Check-out date missing!"
    # assert details.get("total_price") != "Not Available", "Total price missing!"
