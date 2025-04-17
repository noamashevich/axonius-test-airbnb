def log_listing(listing: dict, title: str):
    """
    Print listing details in a readable format.
    """
    if listing:
        print(f"\n{title}:")
        print(f"  - ID: {listing.get('id')}")
        print(f"  - Name: {listing.get('name')}")
        print(f"  - Description: {listing.get('description')}")
        print(f"  - Total price: {listing.get('price')}")
        print(f"  - Rating: {listing.get('rating')}")

    else:
        print(f"\n{title}: No apartments found.")

def print_reservation_details(details: dict):
    """
    Prints reservation details in a clear and clean format.
    Args: details (dict): Dictionary containing reservation details.
    """
    print("\nReservation Details:")
    print("-" * 50)
    for key, value in details.items():
        key_pretty = key.replace("_", " ").capitalize()

        if not value or value == "Not Found":
            value = "Not Available"

        if isinstance(value, str):
            value = " ".join(value.split())

        print(f"{key_pretty:<15}: {value}")
    print("-" * 50 + "\n")
