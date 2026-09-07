import requests
import json
from datetime import datetime
import time
import csv
import os

def get_current_weather(api_key, city_id):
    """
    Get current weather conditions for a specified city
    
    Parameters:
    api_key (str): OpenWeatherMap API key
    city_id (str): City ID
    
    Returns:
    dict: Dictionary containing weather information, or None if error occurs
    """
    # Build API URL
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    url = f"{base_url}?id={city_id}&appid={api_key}&units=metric"  # Add units=metric to get Celsius directly
    
    try:
        # Send GET request
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: API request failed, status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Network request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None

def extract_weather_info(weather_data):
    """
    Extract required weather information from weather data
    
    Parameters:
    weather_data (dict): Complete weather data returned by API
    
    Returns:
    dict: Dictionary containing extracted weather information
    """
    if not weather_data:
        return None
    
    try:
        # Extract the first element from weather array (usually only one)
        weather_info = weather_data.get('weather', [{}])[0]
        weather_id = weather_info.get('id', 'Unknown')
        weather_main = weather_info.get('main', 'Unknown')
        weather_description = weather_info.get('description', 'Unknown')
        
        # Get current time
        current_time = datetime.now()
        
        # Build result dictionary - includes separate date and time fields
        result = {
            'weather_id': weather_id,
            'weather_main': weather_main,
            'weather_description': weather_description,
            'datetime': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'date': current_time.strftime('%Y-%m-%d'),
            'time': current_time.strftime('%H:%M:%S')  # Time accurate to seconds
        }
        
        return result
        
    except (KeyError, IndexError, TypeError) as e:
        print(f"Data extraction error: {e}")
        return None

def save_to_csv(weather_info, file_path):
    """
    Save weather information to CSV file
    
    Parameters:
    weather_info (dict): Weather information
    file_path (str): CSV file path
    """
    # Check if file exists; if not, create it and write header
    file_exists = os.path.isfile(file_path)
    
    try:
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            # Save date, time (to seconds), weather condition and weather ID
            fieldnames = ['date', 'time', 'weather_main', 'weather_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                print(f"Created new CSV file: {file_path}")
            
            # Write data - using separate date and time fields
            writer.writerow({
                'date': weather_info['date'],
                'time': weather_info['time'],
                'weather_main': weather_info['weather_main'],
                'weather_id': weather_info['weather_id']
            })
            
        return True
        
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        return False

def monitor_macau_weather(api_key, output_path, interval=10):
    """
    Monitor Macau weather information
    
    Parameters:
    api_key (str): OpenWeatherMap API key
    output_path (str): Output CSV file path
    interval (int): Interval between fetches in seconds, default is 10 seconds
    """
    # Macau city ID
    MACAU_CITY_ID = 1821274
    
    print(f"Starting Macau weather monitoring...")
    print(f"Data will be saved to: {output_path}")
    print(f"Fetch interval: {interval} seconds")
    print("Press Ctrl+C to stop monitoring\n")
    
    # Counter to control display frequency
    counter = 0
    
    try:
        while True:
            # Get current time
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Show full information every 10 fetches, otherwise show brief info
            if counter % 10 == 0:
                print(f"[{current_time}] Fetching Macau weather information...")
            
            # Get weather data
            weather_data = get_current_weather(api_key, MACAU_CITY_ID)
            
            if weather_data:
                # Extract required information
                weather_info = extract_weather_info(weather_data)
                
                if weather_info:
                    # Save to CSV file
                    save_success = save_to_csv(weather_info, output_path)
                    
                    # Show detailed information every 10 fetches
                    if counter % 10 == 0:
                        print(f"  Weather condition: {weather_info['weather_main']} (ID: {weather_info['weather_id']})")
                        print(f"  Date: {weather_info['date']}, Time: {weather_info['time']}")
                        print(f"  Data saved to CSV")
                        print(f"  Waiting {interval} seconds before next fetch...\n")
                    else:
                        # Brief display, just a dot for progress
                        print(".", end="", flush=True)
                    
                    counter += 1
                else:
                    print("  Unable to extract weather information")
            else:
                print("  Failed to get weather data")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")
    except Exception as e:
        print(f"Error during monitoring: {e}")

def main():
    """
    Main function - set parameters and start monitoring
    """
    # API key
    API_KEY = "5796abbde9106b7da4febfae8c44c232"  # Please ensure this API key is valid
    
    # Specify output path directly - modify this path to your desired location
    # Example paths:
    # Windows: 
    output_csv_path = r"D:/School/MPU_Master/BusData/get_weather/macau_weather.csv"  # Change to your actual path
    # Mac/Linux: 
    # output_csv_path = "/home/username/weather_data/macau_weather.csv"
    
    # Ensure directory exists
    directory = os.path.dirname(output_csv_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    
    # Confirm path
    print(f"Data will be saved to: {os.path.abspath(output_csv_path)}")
    
    # Start monitoring
    monitor_macau_weather(API_KEY, output_csv_path, interval=10)

if __name__ == "__main__":
    main()