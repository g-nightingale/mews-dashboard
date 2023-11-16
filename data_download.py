import requests
import json
import utils as ut
from datetime import datetime, timedelta
import db_utils as db

# https://mews-systems.gitbook.io/connector-api/operations/reservations

# Function to get the first and last moment of a month
def get_start_end_dates(year, month):
    # First moment of the given month
    start_date = datetime(year, month, 1)
    # First moment of the next month
    if month == 12:
        end_date = datetime(year+1, 1, 1)
    else:
        end_date = datetime(year, month+1, 1)
    # Last moment of the given month is right before the first moment of the next month
    end_date = end_date - timedelta(seconds=1)
    return start_date, end_date

def get_historical_api_data():
    """
    Get historical data from Mews API.
    """

    # Load config dict
    config = ut.load_config()

    # Get the current date
    now = datetime.utcnow()

    # List to hold the date ranges
    date_ranges = []

    # Generate dates for the previous twelve months
    for i in range(1, 13):
        # Calculate the year and month for the previous month
        year = (now.year - (now.month - i <= 0))
        month = (now.month - i) % 12 or 12
        # Get the start and end dates
        start_date, end_date = get_start_end_dates(year, month)
        # Add the dates to the list with formatting
        date_ranges.append({
            "StartUtc": start_date.strftime("%Y-%m-%dT00:00:00Z"),  # Start of the month at 00:00:00
            "EndUtc": end_date.strftime("%Y-%m-%dT23:59:59Z"),  # End of the month at 23:59:59
        })

    # Print the date ranges
    for date_range in date_ranges:
        print(f'StartUtc: {date_range["StartUtc"]}, EndUtc: {date_range["EndUtc"]}')

        # Request data
        body = {
            "ClientToken": config['client_token'],
            "AccessToken": config['access_token'],
            "Client": config['client'],
            "UpdatedUtc": {
                "StartUtc": date_range["StartUtc"],
                "EndUtc": date_range["EndUtc"]
            },
            "Limitation":{
                "Count": config['record_limit']
            },
        }

        # Make a POST request to the API
        response = requests.post(config['url'], json=body)

        data = {}
        # Check if the request was successful
        if response.status_code == 200:
            # Response is OK. Do something with the data.
            data = response.json()
            # print(json.dumps(data, indent=4))
        else:
            # There was an error.
            print("Error:", response.status_code, response.text)

        formatted_data = ut.process_mews_data(data)
        db.insert_into_reservations_table(formatted_data)

if __name__ == '__main__':
    get_historical_api_data()