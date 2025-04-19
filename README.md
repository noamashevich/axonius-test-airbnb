Please run: pytest -s --headed --browser=chromium   | on the terminal

🧠 How It Works:

Test 1: Full Reservation Flow
Open Airbnb homepage.

Enter location, dates, guests.

Validate that the URL matches the parameters.

Capture backend API call (StaysSearch).

Parse API and find the highest-rated apartment.

Open the apartment's listing directly.

Handle and close popups if needed.

Scroll to the reservation box.

Extract reservation details like price, guests, dates.

Click "Reserve" and validate reservation consistency.

Test 2: Search and Analyze
Search apartments based on location, dates, guests.

Validate the search URL reflects the criteria.

Capture backend StaysSearch API call.

Find and log:

The cheapest apartment

The highest-rated apartment

Ensure results exist and are valid.


📋 Example Output
bash
Copy
Top Rated Apartment:
  - ID: 1263553043616411164
  - Name: Amazing 2BR with Sea View
  - Description: Newly renovated apartment in Tel Aviv
  - Price per night: ₪441
  - Total price: ₪1053
  - Rating: 5.0

Reservation Details:
--------------------------------------------------
Price per night : ₪441
Total price     : ₪1053
Guests          : 2 guests
Check in        : 2025-05-15
Check out       : 2025-05-18
--------------------------------------------------
🏗️ Technologies Used
Python 3.10+

Playwright (sync API)

Pytest

Requests

Base64

urllib.parse

re

difflib

⚡ Useful Commands

Task	Command
Install Playwright Browsers	playwright install
Run tests normally	pytest
Run tests visible (headed)	pytest --headed
Run only a single test	pytest tests/test_airbnb_reservation.py::test_airbnb_reservation_flow

✍️ Author
Noa Mashevich
Automation Engineer | Python Developer 

📚 Notes
The project uses dynamic scrolling and popup auto-handling because Airbnb often loads elements lazily.

Fuzzy URL matching handles minor differences in location names.

The project is ready to be extended to Booking.com, Expedia, or any other similar site easily!