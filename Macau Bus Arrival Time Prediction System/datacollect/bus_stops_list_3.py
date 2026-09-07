import os
import requests
import json
from datetime import datetime, timezone, timedelta
import time
import pandas as pd

url_route = 'https://bis.dsat.gov.mo:37812/macauweb/getRouteData.html'

timezone_offset = 8
tzinfo = timezone(timedelta(hours=timezone_offset))

def generate_token():
    now = datetime.now(tzinfo)
    year_str = now.strftime("%Y")
    date_str = now.strftime("%m%d")
    time_str = now.strftime("%H%M")
    token = '8aa3' + year_str + '5e0806ec' + date_str + '76af63897e1f' + time_str + '83cdc1fe'
    return token
# 8aa3 2025 5e0806ec 0226 76af63897e1f 1433 83cdc1fe


request_param = {
    'action': 'sd',
    'routeName': '3',
    'dir': '0',
    'lang': 'en',
    'routeType': '0',
    'device': 'web'
}

def fetch_data(headers_route):
    try:
        response_route = requests.post(url_route, headers=headers_route, data=request_param, verify=True)
        response_route .raise_for_status()
        return response_route.json()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def extract_mappings(route_json):
    mappings = []
    for i, entry in  enumerate(route_json['data']['routeInfo']):
        station = entry.get('staCode', '')
        mappings.append((i, station))
    return mappings

def save_to_csv(mappings, file_path):
    df = pd.DataFrame(mappings, columns=['staNum', 'staCode'])
    df.to_csv(file_path, index=False)

def main():
    token = generate_token()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    headers_route = {
        'User-Agent': user_agent,
        'Token': token
    }

    route_json = fetch_data(headers_route)

    if route_json:
        mappings = extract_mappings(route_json)
        outputfile = 'D:/School/MPU_Master/BusData/3/Data/bus_stops.csv'
        save_to_csv(mappings, outputfile)

if __name__ == "__main__":
    main()
