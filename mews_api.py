import requests
import json
import utils as ut

# https://mews-systems.gitbook.io/connector-api/operations/reservations

def get_api_data():
    """
    Get data from Mews API.
    """

    # Load config dict
    config = ut.load_config()

    # Request data
    body = {
        "ClientToken": config['client_token'],
        "AccessToken": config['access_token'],
        "Client": config['client'],
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

    return data


if __name__ == '__main__':
    data = get_api_data()
    print(json.dumps(data['Reservations'][0], indent=4))
    