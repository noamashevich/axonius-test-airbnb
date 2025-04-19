import pytest
from utils.date_utils import validate_date_logic
from utils.logger_utils import log_listing, print_reservation_details
from pages.search_page import AirbnbPage
from pages.airbnb_reservation import AirbnbReservationPage
from pages.components.api_results_analyzer import ApiResultsAnalyzer

@pytest.mark.parametrize(
    "location, check_in, check_out, guests, country_code, phone_number",
    [
        ("Tel Aviv", "2025-05-15", "2025-05-18", {"adults": 2, "children": 1}, '93AF', '0542341121'),
    ]
)
def test_airbnb_reservation_flow(page, location, check_in, check_out, guests, country_code, phone_number):
    """
    End-to-end test for Airbnb reservation flow:
    1. Search apartments
    2. Analyze API results
    3. Open the top-rated apartment
    4. Extract reservation details
    5. Complete reservation process
    """

    # Arrange
    search_page = AirbnbPage(page)
    analyzer = ApiResultsAnalyzer(page)
    reservation_page = AirbnbReservationPage(page)

    # Step 1: Search for apartments
    search_page.go_to_homepage()
    analyzer.start_capture_api_request()

    search_page.enter_location(location)
    validate_date_logic(check_in, check_out)
    search_page.select_dates(check_in, check_out)
    search_page.select_guests(**guests)
    search_page.search()

    # Wait for search results
    page.wait_for_url(lambda url: "s=" in url)
    page.wait_for_selector('[itemprop="itemListElement"]', timeout=7000)

    # Step 2: Validate search URL parameters
    search_page.validate_url_contains({
        "location": location,
        "checkin": check_in,
        "checkout": check_out,
        **guests
    })

    analyzer.fetch_api_results()

    # Step 3: Pick top-rated apartment
    top_rated = analyzer.get_top_rated_from_api()
    assert top_rated is not None, "No top-rated apartment found."
    assert top_rated["id"] is not None, "Top-rated apartment has no ID."

    # Step 4: Go to the listing page
    reservation_page.go_to_listing(top_rated["id"], check_in, check_out, guests)

    # Step 5: Extract reservation details
    reservation_data = reservation_page.get_reservation_data()
    print_reservation_details(reservation_data)

    # Validate reservation details
    assert reservation_data.get("price_per_night") != "Not Available", "Price per night not found!"
    assert reservation_data.get("total_price") != "Not Available", "Total price not found!"
    assert reservation_data.get("guests") != "Not Available", "Guests info not found!"
    assert reservation_data.get("check_in") == check_in, "Check-in date mismatch!"
    assert reservation_data.get("check_out") == check_out, "Check-out date mismatch!"

    # Step 6: Click Reserve button
    reservation_page.click_to_reserve_button()

    # Step 7: Validate reservation form appears
    assert page.locator('[data-testid="login-signup-countrycode"]').is_visible(timeout=5000), "Reservation form did not appear!"

    # Step 8: Fill phone and country details
    reservation_page.fill_reservation_details(country_code, phone_number)

    # Validate phone number was filled correctly
    phone_value = page.locator('input[name="phoneInputphone-login"]').input_value()
    assert phone_value.endswith(phone_number[-7:]), "Phone number not filled correctly!"
