import pytest
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
    reservation_page = AirbnbReservationPage(page)

    # Step 1: Search for apartments
    search_page.go_to_homepage()
    analyzer.start_capture_api_request()

    search_page.enter_location(location)
    search_page.select_dates(check_in, check_out)
    search_page.select_guests(**guests)
    search_page.search()

    analyzer.fetch_api_results()

    # Step 2: Pick top-rated apartment
    top_rated = analyzer.get_top_rated_from_api()
    assert top_rated is not None, "No top-rated apartment found."
    assert top_rated["id"] is not None, "Top-rated apartment has no ID."

    # Step 3: Go to the listing page
    reservation_page.go_to_listing(top_rated["id"], check_in, check_out, guests)

    # Step 4: Save reservation details
    details = reservation_page.save_reservation_details()
    print_reservation_details(details)

    # Step 5: Basic validation
    assert details.get("check_in") != "Not Available", "Check-in date missing!"
    assert details.get("check_out") != "Not Available", "Check-out date missing!"
