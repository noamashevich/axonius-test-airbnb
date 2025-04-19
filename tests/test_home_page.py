from utils.date_utils import validate_date_logic
from utils.logger_utils import log_listing
from pages.search_page import AirbnbPage
from pages.components.api_results_analyzer import ApiResultsAnalyzer
import pytest


@pytest.mark.parametrize(
    "location, check_in, check_out, guests",
    [
        ("Tel Aviv", "2025-04-19", "2025-04-20", {"adults": 2}),
    ]
)
def test_airbnb_search_and_analyze(page, location, check_in, check_out, guests):
    """
    End-to-end test for Airbnb search and backend API analysis:
    1. Search apartments
    2. Validate URL reflects search parameters
    3. Capture and analyze API response
    4. Find cheapest and top-rated apartments
    """

    # Arrange
    search_page = AirbnbPage(page)
    analyzer = ApiResultsAnalyzer(page)

    # Step 1: Navigate to Airbnb homepage and start capturing API requests
    search_page.go_to_homepage()
    analyzer.start_capture_api_request()

    # Step 2: Enter search details
    search_page.enter_location(location)
    validate_date_logic(check_in, check_out)
    search_page.select_dates(check_in, check_out)
    search_page.select_guests(**guests)
    search_page.search()

    # Step 3: Wait for search results
    page.wait_for_url(lambda url: "s=" in url)
    page.wait_for_selector('[itemprop="itemListElement"]', timeout=7000)

    # Step 4: Validate URL parameters
    search_page.validate_url_contains({
        "location": location,
        "checkin": check_in,
        "checkout": check_out,
        **guests
    })

    # Step 5: Fetch and analyze API results
    analyzer.fetch_api_results()
    cheapest = analyzer.get_cheapest_from_api()
    top_rated = analyzer.get_top_rated_from_api()

    # Step 6: Log the details
    log_listing(cheapest, "Cheapest Apartment")
    log_listing(top_rated, "Top Rated Apartment")

    # Step 7: Validations
    assert cheapest is not None, "No cheapest apartment found."
    assert top_rated is not None, "No top-rated apartment found."

    assert cheapest.get("id") is not None, "Cheapest apartment has no ID!"
    assert top_rated.get("id") is not None, "Top-rated apartment has no ID!"

    assert cheapest.get("name") not in (None, ""), "Cheapest apartment has no name!"
    assert top_rated.get("name") not in (None, ""), "Top-rated apartment has no name!"

    assert cheapest.get("price") not in (None, ""), "Cheapest apartment has no price!"
    assert top_rated.get("price") not in (None, ""), "Top-rated apartment has no price!"

