import requests
import os 

SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.environ.get("SHEETY_USERS_ENDPOINT")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")


class DataManager:

    def __init__(self):
        self.sheets_data = {}
        self.customer_data = []

    def get_sheets_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        response.raise_for_status()

        self.sheets_data = response.json()["prices"]
        return self.sheets_data

    def update_iata_data(self):
        for city in self.sheets_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_data)
            print(response.text)

    def update_price_data(self):
        for city in self.sheets_data:
            new_data = {
                "price": {
                    "lowestPrice": city["lowestPrice"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_data)
            print(response.text)

    def get_customer_emails(self):
        customer_endpoint = SHEETY_USERS_ENDPOINT
        response = requests.get(url=customer_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
