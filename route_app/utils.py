import requests
import pandas as pd
from decouple import config
from django.conf import settings
import os
from fuzzywuzzy import process

# Load fuel prices data globally for the API
FUEL_PRICES_FILE = os.path.join(settings.BASE_DIR, 'route_app', 'file_dir', 'fuel_prices.csv')
fuel_prices_data = pd.read_csv(FUEL_PRICES_FILE)

# Constants
VEHICLE_RANGE_MILES = 500
VEHICLE_MPG = 10

#function to fetch the route, stops and distance from Open Route API
def get_route_details(start, finish):
    api_key = config("API_KEY")
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



def find_optimal_locations(distances_miles, addresses):
    optimal_locations = []  # Initialize an empty list for optimal locations
    cumulative_distance = 0  # Variable to track the cumulative distance

    for distance_miles, address in zip(distances_miles, addresses):
        cumulative_distance += distance_miles  # Add the current distance to the cumulative total
        if cumulative_distance >= 500:  # Check if the cumulative distance has reached or exceeded 500 miles
            optimal_locations.append(address)  # Add the corresponding address to the list

    return optimal_locations



# Function to calculate cost based on optimal locations
def calculate_total_amount(optimal_locations):
    total_amount = 0 

    # List of addresses from CSV
    address_list = fuel_prices_data['Address'].tolist()

    # Iterate over each optimal location
    for address in optimal_locations:

        # Using Fuzzy match to match the address with the addresses in the CSV
        best_match, score = process.extractOne(address, address_list)
        
        #score > 80 means a strong match
        if score >=60:

            # Get the corresponding retail price for the best match
            fuel_price_row = fuel_prices_data[fuel_prices_data['Address'] == best_match]
            retail_price = fuel_price_row['Retail Price'].values[0]
        else:

            # use average reatail price if no good match is found
            retail_price = 3.1
        
        # Perform the cost calculation: (500 / 10) * retail price
        cost = (500 / 10) * retail_price
        total_amount += cost  # Add the cost for this address to total amount

    return total_amount
