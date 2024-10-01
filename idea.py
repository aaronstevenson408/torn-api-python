import os
import requests
import time
import logging
import json
from dotenv import load_dotenv
from tabulate import tabulate
from collections import deque

# Set up logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
API_KEY = os.getenv('full')
logging.debug(f"API_KEY loaded: {'*' * len(API_KEY)}")

# API endpoints
BASE_URL = "https://api.torn.com"
USER_ENDPOINT = f"{BASE_URL}/user/"
TORN_ENDPOINT = f"{BASE_URL}/torn/"
MARKET_ENDPOINT = f"{BASE_URL}/market/"

# Global rate limiting
MAX_CALLS_PER_MINUTE = 100
call_timestamps = deque(maxlen=MAX_CALLS_PER_MINUTE)

def rate_limited_call(url):
    current_time = time.time()
    
    if len(call_timestamps) == MAX_CALLS_PER_MINUTE:
        oldest_call = call_timestamps[0]
        if current_time - oldest_call < 60:
            sleep_time = 60 - (current_time - oldest_call)
            logging.debug(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
    
    response = requests.get(url)
    call_timestamps.append(time.time())
    return response

def get_player_data_and_items():
    logging.debug("Fetching player data and city shop items")
    url = f"{TORN_ENDPOINT}?selections=items,cityshops&key={API_KEY}"
    response = rate_limited_call(url)
    data = response.json()
    
    # Convert dict_keys to a list before JSON serialization
    logging.debug(f"API response structure: {json.dumps(list(data.keys()), indent=2)}")
    
    if 'items' not in data or 'cityshops' not in data:
        logging.error("Required data not found in API response")
        return []

    items_data = data['items']
    cityshops_data = data['cityshops']
    
    items = []
    for shop_id, shop_data in cityshops_data.items():
        shop_name = shop_data.get('name', 'Unknown')
        inventory = shop_data.get('inventory', {})
        
        for item_id, item_data in inventory.items():
            if item_id in items_data:
                items.append({
                    'id': item_id,
                    'name': items_data[item_id]['name'],
                    'shop_price': item_data['price'],
                    'in_stock': item_data.get('in_stock', 0),
                    'shop_id': shop_id,
                    'shop_name': shop_name
                })

    logging.debug(f"Total items found: {len(items)}")
    return items

def get_market_prices(item_ids):
    logging.debug(f"Fetching market prices for {len(item_ids)} items")
    prices = {}
    for item_id in item_ids:
        url = f"{MARKET_ENDPOINT}{item_id}?selections=bazaar&key={API_KEY}"
        response = rate_limited_call(url)
        data = response.json()
        if 'bazaar' in data and data['bazaar']:
            prices[item_id] = data['bazaar'][0]['cost']
    return prices

def calculate_potential_profit(items, market_prices):
    logging.debug("Calculating potential profit")
    profit_data = []

    for item in items:
        if item['id'] in market_prices:
            market_price = market_prices[item['id']]
            potential_profit = market_price - item['shop_price']
            profit_data.append({
                'id': item['id'],
                'name': item['name'],
                'shop_price': item['shop_price'],
                'market_price': market_price,
                'potential_profit': potential_profit,
                'in_stock': item['in_stock'],
                'shop_id': item['shop_id'],
                'shop_name': item['shop_name']
            })

    return sorted(profit_data, key=lambda x: x['potential_profit'], reverse=True)

def main():
    logging.info("Starting Torn RPG Profit Scanner")

    items = get_player_data_and_items()
    if not items:
        logging.error("No items found. Exiting program.")
        return

    print(f"Total items found: {len(items)}")

    item_ids = [item['id'] for item in items]
    market_prices = get_market_prices(item_ids)

    profit_data = calculate_potential_profit(items, market_prices)

    headers = ["ID", "Name", "Shop", "Shop Price", "Market Price", "Potential Profit", "In Stock"]
    table_data = [[item['id'], item['name'], item['shop_name'], f"${item['shop_price']}", 
                   f"${item['market_price']}", f"${item['potential_profit']}", item['in_stock']] 
                  for item in profit_data]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    logging.info("Profit data table generated")
    logging.debug(f"Top 5 profitable items: {profit_data[:5]}")

    logging.info("Torn RPG Profit Scanner completed")

if __name__ == "__main__":
    main()