import requests
import pandas as pd
from decouple import config

# Load fuel prices data globally for the API
FUEL_PRICES_FILE = 'file_dir/fuel_prices.csv'
fuel_prices_data = pd.read_csv(FUEL_PRICES_FILE)

# Constants
VEHICLE_RANGE_MILES = 500
VEHICLE_MPG = 10

#function to fetch the route from Open Route API
def get_route(start, finish):
    api_key = config("API_KEY")
    base_url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    
    params = {
        'api_key': api_key,
        'start': f"{start[0]},{start[1]}",
        'end': f"{finish[0]},{finish[1]}" 
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        print("Worked")
        return response.json()
    return None
