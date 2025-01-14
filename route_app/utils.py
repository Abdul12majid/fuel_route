import requests
import pandas as pd
from decouple import config

# Load fuel prices data globally for the API
FUEL_PRICES_FILE = 'file_dir/fuel_prices.csv'
fuel_prices_data = pd.read_csv(FUEL_PRICES_FILE)

# Constants
VEHICLE_RANGE_MILES = 500
VEHICLE_MPG = 10

#function to fetch the route, stops and distance from Open Route API
def get_route_details(start, finish):
    api_key = '5b3ce3597851110001cf6248df093dc1726d48efb78af576218be836'
    base_url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    
    params = {
        'api_key': api_key,
        'start': f"{start[0]},{start[1]}",
        'end': f"{finish[0]},{finish[1]}"
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            # get total distance
            distance_meters = data['features'][0]['properties']['summary']['distance']
            distance_miles = distance_meters * 0.000621371  # Convert meters to miles
            
            # get steps
            steps = data['features'][0]['properties']['segments'][0]['steps']
            
            # Initialize empty lists for addresses and distances
            addresses = []
            distances_miles = []  # Store distances in miles
            
            for step in steps:
                step_distance_meters = step['distance']  # Step distance in meters
                step_distance_miles = step_distance_meters * 0.000621371  # Convertion to miles
                step_name = step.get('name', 'Unnamed road')  # Use 'unnnamed' if actual name is missing
                
                
                addresses.append(step_name)
                distances_miles.append(step_distance_miles)
            
            return {
                "total_distance_miles": distance_miles,
                "addresses": addresses,
                "distances_miles": distances_miles
            }
        except (KeyError, IndexError):
            print("Error: Could not extract route details from response. Check response format.")
            return None
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return None
