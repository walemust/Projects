import requests
import json
import os
from src.config import API_KEY, BASE_URL


city = {'San Antonio','San Francisco', 'Alva'}
state = {'TX','CA','FL'}


def extract_properties(cities=['San Antonio', 'San Francisco', 'Alva'],
                       states=['TX', 'CA', 'FL']):
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }

    
    os.makedirs("data/raw", exist_ok=True)

    
    for city, state in zip(cities, states):
        params = {"city": city, "state": state}
        print(f"Fetching properties data from {city}, {state}...")

        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            
            safe_city = city.replace(" ", "_")
            filename = f"data/raw/properties_{safe_city}_{state}.json"

            
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)

            print(f"Saved: {filename}")
        else:
            print(f"Failed for {city}, {state}: {response.status_code} - {response.text}")


extract_properties()