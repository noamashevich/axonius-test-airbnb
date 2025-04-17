from datetime import datetime

def to_airbnb_date_label(date_str: str) -> str:
    """
    Converts a date string like '2025-04-17' to Airbnb's aria-label format.
    :param date_str: Date string in format YYYY-MM-DD
    :return: Formatted string like 'Thursday, April 17, 2025'
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d, %A, %B %Y")  # Airbnb format

def validate_date_logic(check_in: str, check_out: str):
    """
    Validates that the check-out date is later than the check-in date.
    :param check_in: Check-in date as string 'YYYY-MM-DD'
    :param check_out: Check-out date as string 'YYYY-MM-DD'
    :raises AssertionError if the logic is invalid
    """
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    assert check_out_date > check_in_date, f"Check-out date ({check_out}) must be later than check-in date ({check_in})"