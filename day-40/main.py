from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "BLR"

sheet_data = data_manager.get_sheets_data()

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_iata_code(city_names)
    data_manager.update_iata_data()
    sheet_data = data_manager.get_sheets_data()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6 * 30))

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

for destination_code in destinations:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code,
        from_time=tomorrow,
        to_time=six_months_from_today
    )

    if flight is not None and flight.price < destinations[destination_code]["price"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]
        message = f"Low price alert! Only ₹{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} " \
                  f"to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} " \
                  f"to {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        link = f"https://www.google.co.uk/flights?hl=en#flt=" \
               f"{flight.origin_airport}.{flight.destination_airport}." \
               f"{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

        notification_manager.send_emails(emails, message, link)
