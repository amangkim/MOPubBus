import os
import requests
import json
from datetime import datetime, timezone, timedelta
import time
import pandas as pd
import threading
import logging
import hashlib
import csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bus_crawler_fixed.log'),
        logging.StreamHandler()
    ]
)

class WeatherMonitor:
    """Weather monitoring class"""
    def __init__(self, api_key, city_id=1821274, output_path=None):
        self.api_key = api_key
        self.city_id = city_id
        self.output_path = output_path or "D:/School/MPU_Master/BusData/get_weather/grandprix/macau_weather_grandprix.csv"
        self.current_weather = "Unknown"
        self.current_weather_id = "Unknown"
        
        # Ensure directory exists
        directory = os.path.dirname(self.output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Weather Monitor - Directory created: {directory}")
        
        # Initialize CSV file
        self.init_weather_csv()
        
        # Start weather monitoring thread
        self.weather_thread = threading.Thread(target=self.monitor_weather, daemon=True)
        self.weather_thread.start()
        logging.info("Weather monitoring thread started")

    def init_weather_csv(self):
        """Initialize weather CSV file"""
        if not os.path.exists(self.output_path):
            try:
                with open(self.output_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['date', 'time', 'weather_main', 'weather_id']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                logging.info(f"Weather Monitor - New CSV file created: {self.output_path}")
            except Exception as e:
                logging.error(f"Weather Monitor - Failed to create CSV file: {e}")

    def get_current_weather(self):
        """Get current weather"""
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        url = f"{base_url}?id={self.city_id}&appid={self.api_key}&units=metric"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logging.warning(f"Weather API request failed, status code: {response.status_code}")
                return None
        except Exception as e:
            logging.warning(f"Failed to get weather data: {e}")
            return None

    def extract_weather_info(self, weather_data):
        """Extract weather information"""
        if not weather_data:
            return None
        
        try:
            weather_info = weather_data.get('weather', [{}])[0]
            weather_id = weather_info.get('id', 'Unknown')
            weather_main = weather_info.get('main', 'Unknown')
            
            current_time = datetime.now()
            
            return {
                'weather_id': weather_id,
                'weather_main': weather_main,
                'date': current_time.strftime('%Y-%m-%d'),
                'time': current_time.strftime('%H:%M:%S')
            }
        except Exception as e:
            logging.error(f"Failed to extract weather information: {e}")
            return None

    def save_weather_data(self, weather_info):
        """Save weather data to CSV"""
        try:
            with open(self.output_path, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['date', 'time', 'weather_main', 'weather_id']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    'date': weather_info['date'],
                    'time': weather_info['time'],
                    'weather_main': weather_info['weather_main'],
                    'weather_id': weather_info['weather_id']
                })
            return True
        except Exception as e:
            logging.error(f"Failed to save weather data: {e}")
            return False

    def monitor_weather(self):
        """Monitor weather"""
        logging.info("Started monitoring Macau weather information")
        counter = 0
        
        while True:
            try:
                weather_data = self.get_current_weather()
                
                if weather_data:
                    weather_info = self.extract_weather_info(weather_data)
                    
                    if weather_info:
                        # Update current weather
                        self.current_weather = weather_info['weather_main']
                        self.current_weather_id = weather_info['weather_id']
                        
                        # Save to CSV
                        self.save_weather_data(weather_info)
                        
                        # Display log every 10 times
                        if counter % 10 == 0:
                            logging.info(f"Weather Monitor - Current weather: {self.current_weather} (ID: {self.current_weather_id})")
                        
                        counter += 1
                
                time.sleep(10)  # Get data every 10 seconds
                
            except Exception as e:
                logging.error(f"Weather monitoring exception: {e}")
                time.sleep(30)

class FixedBusRouteCrawler:
    def __init__(self, route_config, weather_monitor):
        """
        Fixed version of bus route crawler
        """
        self.config = route_config
        self.weather_monitor = weather_monitor
        
        # Initialize state variables
        self.previous_bus_data = {}
        self.arrival_records = pd.DataFrame(columns=[
            'startStation', 'endStation', 'date', 'time', 'weekday', 
            'passengerFlow', 'trafficCondition', 'busPlate', 'passbyNum', 
            'arrivalDuration', 'weather'  # Added weather column
        ])
        self.start_times = {}
        self.start_stations = {}
        self.bus_ready = {}
        self.station_list = []
        self.firstrun = True
        self.consecutive_failures = 0
        self.max_consecutive_failures = 3
        
        # Timezone settings
        self.timezone_offset = 8
        self.tzinfo = timezone(timedelta(hours=self.timezone_offset))
        
        # Ensure save directory exists
        os.makedirs(os.path.dirname(self.config['file_path']), exist_ok=True)
        
        # If file exists, load existing data
        if os.path.exists(self.config['file_path']):
            try:
                self.arrival_records = pd.read_csv(self.config['file_path'])
                logging.info(f"Route {self.config['route_name']} - Loaded existing data: {self.config['file_path']}")
            except Exception as e:
                logging.warning(f"Route {self.config['route_name']} - Failed to load existing data, creating new file: {e}")
                self.arrival_records = pd.DataFrame(columns=[
                    'startStation', 'endStation', 'date', 'time', 'weekday', 
                    'passengerFlow', 'trafficCondition', 'busPlate', 'passbyNum', 
                    'arrivalDuration', 'weather'  # Added weather column
                ])

    def generate_correct_token(self):
        """Generate correct access token - fixed version"""
        now = datetime.now(self.tzinfo)
        
        # Generate corresponding token based on route name
        route_tokens = {
            '3': f"5403{now.strftime('%Y')}ed03b5dc{now.strftime('%m%d')}dad693993d97{now.strftime('%H%M')}e83bb5bd",
            '15': f"bf18{now.strftime('%Y')}e3242849{now.strftime('%m%d')}120bbf6f5ea4{now.strftime('%H%M')}43655a97",
            '26': f"238d{now.strftime('%Y')}832f5539{now.strftime('%m%d')}fe00fa279eb6{now.strftime('%H%M')}bb6ca85c",
            '73': f"05f0{now.strftime('%Y')}4ffbfe57{now.strftime('%m%d')}87601f711328{now.strftime('%H%M')}268a3358",
            'AP1': f"2420{now.strftime('%Y')}914cb467{now.strftime('%m%d')}34f9782db1b1{now.strftime('%H%M')}a51f08ea"
        }
        
        return route_tokens.get(self.config['route_name'], hashlib.md5(f"{now.timestamp()}".encode()).hexdigest())

    def fetch_data_with_fixes(self):
        """Fixed version of data fetching"""
        try:
            token = self.generate_correct_token()
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
            
            headers_bus = {
                'User-Agent': user_agent,
                'Token': token,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'https://bis.dsat.gov.mo/',
                'Origin': 'https://bis.dsat.gov.mo'
            }
            
            headers_traffic = {
                'User-Agent': user_agent,
                'Referer': 'https://bis.dsat.gov.mo/'
            }
            
            # Set reasonable timeout
            timeout = (10, 15)
            
            logging.debug(f"Route {self.config['route_name']} - Using token: {token}")
            
            # Get bus data - using more compatible request method
            response_bus = requests.post(
                self.config['bus_url'], 
                headers=headers_bus, 
                data=self.config['request_param'], 
                verify=True,
                timeout=timeout,
                allow_redirects=True
            )
            
            # Get traffic data
            response_traffic = requests.get(
                self.config['traffic_url'], 
                headers=headers_traffic, 
                verify=True,
                timeout=timeout
            )
            
            # Log response status
            logging.info(f"Route {self.config['route_name']} - Bus response status: {response_bus.status_code}")
            logging.info(f"Route {self.config['route_name']} - Traffic response status: {response_traffic.status_code}")
            
            # Check status codes
            if response_bus.status_code != 200 or response_traffic.status_code != 200:
                logging.warning(f"Route {self.config['route_name']} - HTTP status code abnormal")
                if response_bus.status_code != 200:
                    logging.debug(f"Route {self.config['route_name']} - Bus response content: {response_bus.text[:200]}")
                if response_traffic.status_code != 200:
                    logging.debug(f"Route {self.config['route_name']} - Traffic response content: {response_traffic.text[:200]}")
                return None, None
            
            # Safely parse JSON
            try:
                bus_json = response_bus.json()
                logging.debug(f"Route {self.config['route_name']} - Bus JSON parsed successfully")
            except json.JSONDecodeError as e:
                logging.error(f"Route {self.config['route_name']} - Bus data JSON parsing failed: {e}")
                logging.debug(f"Route {self.config['route_name']} - Bus raw response: {response_bus.text[:500]}")
                return None, None
                
            try:
                traffic_json = response_traffic.json()
                logging.debug(f"Route {self.config['route_name']} - Traffic JSON parsed successfully")
            except json.JSONDecodeError as e:
                logging.error(f"Route {self.config['route_name']} - Traffic data JSON parsing failed: {e}")
                return None, None
            
            # Fixed data structure validation
            if self.fixed_validate_json_structure(bus_json, traffic_json):
                self.consecutive_failures = 0
                return bus_json, traffic_json
            else:
                return None, None
            
        except requests.exceptions.Timeout:
            logging.warning(f"Route {self.config['route_name']} - Request timeout")
            return None, None
        except requests.exceptions.ConnectionError as e:
            logging.warning(f"Route {self.config['route_name']} - Connection error: {e}")
            return None, None
        except requests.RequestException as e:
            logging.error(f"Route {self.config['route_name']} - Data fetching failed: {e}")
            return None, None
        except Exception as e:
            logging.error(f"Route {self.config['route_name']} - Unknown error occurred: {e}")
            return None, None

    def fixed_validate_json_structure(self, bus_json, traffic_json):
        """Fixed version of data structure validation"""
        try:
            # Check if it's a dictionary
            if not isinstance(bus_json, dict):
                logging.error(f"Route {self.config['route_name']} - bus_json is not a dictionary")
                return False
                
            if not isinstance(traffic_json, dict):
                logging.error(f"Route {self.config['route_name']} - traffic_json is not a dictionary")
                return False
            
            # Check bus data structure - Fix: allow data to be empty string
            if 'data' not in bus_json:
                logging.error(f"Route {self.config['route_name']} - bus_json missing 'data' field")
                return False
            
            bus_data = bus_json['data']
            
            # Fix: if bus data is empty string, it means no vehicle data, which is normal
            if isinstance(bus_data, str) and bus_data == "":
                logging.info(f"Route {self.config['route_name']} - Bus data is empty (no vehicles running)")
                # In this case we still return True because it's a valid response
                return True
            
            # If bus_data is a dictionary, check routeInfo
            if isinstance(bus_data, dict):
                if 'routeInfo' not in bus_data:
                    logging.error(f"Route {self.config['route_name']} - bus_data missing 'routeInfo' field")
                    return False
                
                if not isinstance(bus_data['routeInfo'], list):
                    logging.error(f"Route {self.config['route_name']} - bus_data['routeInfo'] is not a list")
                    return False
            else:
                logging.error(f"Route {self.config['route_name']} - bus_data is neither dictionary nor empty string")
                return False
            
            # Check traffic data structure
            if 'data' not in traffic_json:
                logging.error(f"Route {self.config['route_name']} - traffic_json missing 'data' field")
                return False
            
            traffic_data = traffic_json['data']
            
            if not isinstance(traffic_data, dict):
                logging.error(f"Route {self.config['route_name']} - traffic_data is not a dictionary")
                return False
            
            if 'stationInfo' not in traffic_data:
                logging.error(f"Route {self.config['route_name']} - traffic_data missing 'stationInfo' field")
                return False
            
            if not isinstance(traffic_data['stationInfo'], list):
                logging.error(f"Route {self.config['route_name']} - traffic_data['stationInfo'] is not a list")
                return False
            
            logging.debug(f"Route {self.config['route_name']} - Data structure validation successful")
            return True
            
        except Exception as e:
            logging.error(f"Route {self.config['route_name']} - Data structure validation exception: {e}")
            return False

    def process_data_with_empty_handling(self, bus_json, traffic_json):
        """Process data including handling empty data situations"""
        if not bus_json or not traffic_json:
            return
            
        now = datetime.now(self.tzinfo)
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%H:%M:%S")
        weekday = now.weekday()
        
        try:
            # Handle case when bus data is empty
            bus_data = bus_json.get('data')
            if isinstance(bus_data, str) and bus_data == "":
                logging.debug(f"Route {self.config['route_name']} - Currently no buses running")
                return
            
            # Safely access routeInfo
            route_info = bus_data.get('routeInfo', [])
            if not isinstance(route_info, list):
                logging.warning(f"Route {self.config['route_name']} - routeInfo is not a list type")
                return
            
            logging.debug(f"Route {self.config['route_name']} - Processing {len(route_info)} route information entries")
            
            for entry in route_info:
                if not isinstance(entry, dict):
                    continue
                    
                station = entry.get('staCode')
                if not station:
                    continue
                    
                if self.firstrun:
                    self.station_list.append(station)
                    logging.debug(f"Route {self.config['route_name']} - Added station: {station}")
                
                # Safely access busInfo
                bus_info_list = entry.get('busInfo', [])
                if not isinstance(bus_info_list, list):
                    continue
                    
                logging.debug(f"Route {self.config['route_name']} - Station {station} has {len(bus_info_list)} buses")
                    
                for current_info in bus_info_list:
                    if not isinstance(current_info, dict):
                        continue
                        
                    bus_plate = current_info.get('busPlate')
                    if not bus_plate:
                        continue

                    # Process bus status
                    self.process_bus_status(
                        bus_plate, current_info, station, traffic_json, 
                        date_str, time_str, weekday
                    )
                    
            self.firstrun = False
            
        except Exception as e:
            logging.error(f"Route {self.config['route_name']} - Error processing data: {e}")
            self.consecutive_failures += 1

    def process_bus_status(self, bus_plate, current_info, station, traffic_json, date_str, time_str, weekday):
        """Process bus status"""
        try:
            # If this is the first time seeing this bus, set initial state
            if bus_plate not in self.previous_bus_data:
                self.previous_bus_data[bus_plate] = current_info.copy()
                self.bus_ready[bus_plate] = 'no'
                logging.debug(f"Route {self.config['route_name']} - New bus: {bus_plate}, status: {current_info.get('status')}")
                return

            previous_info = self.previous_bus_data[bus_plate]
            
            # Process bus ready state
            if not self.update_bus_ready_state(bus_plate, current_info, previous_info):
                return

            current_status = current_info.get('status')
            previous_status = previous_info.get('status')
            
            logging.debug(f"Route {self.config['route_name']} - Bus {bus_plate} status: {previous_status} -> {current_status}")
            
            # If current status is '0' and previous status was '1', record start time
            if current_status == '0' and previous_status == '1':
                if bus_plate not in self.start_times:
                    self.start_times[bus_plate] = datetime.now(self.tzinfo)
                    self.start_stations[bus_plate] = station
                    logging.info(f"Route {self.config['route_name']} - Bus {bus_plate} departed from station {station}")
                            
            # If current status is '1' and previous status was '0', calculate total arrival time and record
            elif current_status == '1' and previous_status == '0':
                if bus_plate in self.start_times:
                    arrival_duration = (datetime.now(self.tzinfo) - self.start_times[bus_plate]).total_seconds()
                    
                    # Safely get traffic condition
                    traffic_condition = -1
                    station_info = traffic_json.get('data', {}).get('stationInfo', [])
                    for traffic_entry in station_info:
                        if isinstance(traffic_entry, dict) and traffic_entry.get('stationCode') == station:
                            traffic_condition = traffic_entry.get('newRouteTraffic', -1)
                            break
                    
                    # Calculate number of stations passed
                    passby_number = 0
                    try:
                        start_index = self.station_list.index(self.start_stations[bus_plate])
                        end_index = self.station_list.index(station)
                        passby_number = end_index - start_index - 1
                    except (ValueError, AttributeError):
                        passby_number = 0
                    
                    # Get current weather
                    current_weather = self.weather_monitor.current_weather
                    
                    self.record_arrival(
                        station=self.start_stations[bus_plate],
                        endstation=station,
                        date=date_str,
                        time=time_str,
                        weekday=weekday,
                        passenger_flow=current_info.get('passengerFlow', -1),
                        traffic_condition=traffic_condition,
                        bus_plate=bus_plate,
                        passby_number=passby_number,
                        arrival_duration=int(arrival_duration),
                        weather=current_weather  # Added weather parameter
                    )
                    
                    # Clean up state
                    if bus_plate in self.start_times:
                        del self.start_times[bus_plate]
                    if bus_plate in self.start_stations:
                        del self.start_stations[bus_plate]

            self.previous_bus_data[bus_plate] = current_info.copy()
            
        except Exception as e:
            logging.error(f"Route {self.config['route_name']} - Error processing bus status: {e}")

    def update_bus_ready_state(self, bus_plate, current_info, previous_info):
        """Update bus ready state"""
        try:
            current_status = current_info.get('status')
            
            if self.bus_ready[bus_plate] == 'no':
                if current_status == '0':
                    # Bus is already on the road, skip
                    self.previous_bus_data[bus_plate] = current_info.copy()
                    return False
                else:
                    # Bus arrived at station, start preparing
                    self.bus_ready[bus_plate] = 'preparing'
                    self.previous_bus_data[bus_plate] = current_info.copy()
                    return False
                    
            elif self.bus_ready[bus_plate] == 'preparing':
                if current_status == '0':
                    # Bus departed from station, start recording
                    self.bus_ready[bus_plate] = 'ready'
                    logging.info(f"Route {self.config['route_name']} - Bus {bus_plate} ready, starting recording")
                else:
                    self.previous_bus_data[bus_plate] = current_info.copy()
                    return False
                    
            elif self.bus_ready[bus_plate] != 'ready':
                self.previous_bus_data[bus_plate] = current_info.copy()
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Route {self.config['route_name']} - Error updating bus ready state: {e}")
            return False

    def record_arrival(self, station, endstation, date, time, weekday, 
                      passenger_flow, traffic_condition, bus_plate, 
                      passby_number, arrival_duration, weather):
        """Record arrival information"""
        try:
            record = {
                'startStation': station,
                'endStation': endstation,
                'date': date,
                'time': time,
                'weekday': weekday,
                'passengerFlow': passenger_flow,
                'trafficCondition': traffic_condition,
                'busPlate': bus_plate,
                'passbyNum': passby_number,
                'arrivalDuration': arrival_duration,
                'weather': weather  # Added weather field
            }
            
            # Add to DataFrame
            self.arrival_records = pd.concat([
                self.arrival_records, 
                pd.DataFrame([record])
            ], ignore_index=True)
            
            # Save to CSV file
            self.arrival_records.to_csv(self.config['file_path'], index=False)
            
            logging.info(f"Route {self.config['route_name']} - Recorded bus {bus_plate} from {station} to {endstation}, duration {arrival_duration} seconds, weather: {weather}")
            
        except Exception as e:
            logging.error(f"Route {self.config['route_name']} - Failed to record arrival information: {e}")

    def get_smart_interval(self):
        """Intelligent request interval calculation"""
        base_interval = 10  # Base interval 10 seconds to avoid too frequent requests
        
        if self.consecutive_failures > 0:
            # More errors, longer interval
            backoff = min(2 ** self.consecutive_failures, 60)
            return base_interval + backoff
        
        return base_interval

    def run(self):
        """Run crawler"""
        logging.info(f"Started monitoring route {self.config['route_name']}")
        
        while True:
            try:
                bus_json, traffic_json = self.fetch_data_with_fixes()
                
                if bus_json and traffic_json:
                    self.process_data_with_empty_handling(bus_json, traffic_json)
                else:
                    self.consecutive_failures += 1
                    logging.warning(f"Route {self.config['route_name']} - Data fetching failed, consecutive failures: {self.consecutive_failures}")
                    
                # If too many consecutive failures, pause for a while
                if self.consecutive_failures >= self.max_consecutive_failures:
                    wait_time = 120  # Pause for 2 minutes
                    logging.warning(f"Route {self.config['route_name']} - Too many consecutive failures, pausing for {wait_time} seconds")
                    time.sleep(wait_time)
                    self.consecutive_failures = 0
                
                # Dynamic interval
                interval = self.get_smart_interval()
                logging.debug(f"Route {self.config['route_name']} - Waiting {interval} seconds before continuing")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logging.info(f"Route {self.config['route_name']} - Monitoring stopped")
                break
            except Exception as e:
                logging.error(f"Route {self.config['route_name']} - Monitoring loop exception: {e}")
                self.consecutive_failures += 1
                time.sleep(30)  # Wait longer when exception occurs

# Five route configurations
ROUTE_CONFIGS = [
    {
        'route_name': '3',
        'bus_url': 'https://bis.dsat.gov.mo:37812/macauweb/routestation/bus',
        'traffic_url': 'https://bis.dsat.gov.mo:37812/ddbus/common/supermap/routeStation/traffic?device=web&HUID=8c00ad72-bba1-4c25-bd4f-87fd29c3213a&routeCode=00003&direction=0&indexType=00&lang=en&categoryIds=BCAFBD938B8D48B0B3F598B44DD32E6C',
        'request_param': {
            'action': 'dy',
            'routeName': '3',
            'dir': '0',
            'lang': 'zh-tw',
            'routeType': '0',
            'device': 'web'
        },
        'file_path': 'D:/School/MPU_Master/BusData/get_weather/grandprix/arrival_records_3_d0_grandprix.csv'
    },
    {
        'route_name': '15',
        'bus_url': 'https://bis.dsat.gov.mo:37812/macauweb/routestation/bus',
        'traffic_url': 'https://bis.dsat.gov.mo:37812/ddbus/common/supermap/routeStation/traffic?device=web&HUID=fd7444de-b635-400d-bf59-b0793114ebc4&routeCode=00015&direction=0&indexType=00&lang=zh_tw&categoryIds=BCAFBD938B8D48B0B3F598B44DD32E6C',
        'request_param': {
            'action': 'dy',
            'routeName': '15',
            'dir': '0',
            'lang': 'zh-tw',
            'routeType': '2',
            'device': 'web'
        },
        'file_path': 'D:/School/MPU_Master/BusData/get_weather/grandprix/arrival_records_15_grandprix.csv'
    },
    {
        'route_name': '26',
        'bus_url': 'https://bis.dsat.gov.mo:37812/macauweb/routestation/bus',
        'traffic_url': 'https://bis.dsat.gov.mo:37812/ddbus/common/supermap/routeStation/traffic?device=web&HUID=fd7444de-b635-400d-bf59-b0793114ebc4&routeCode=00026&direction=0&indexType=00&lang=zh_tw&categoryIds=BCAFBD938B8D48B0B3F598B44DD32E6C',
        'request_param': {
            'action': 'dy',
            'routeName': '26',
            'dir': '0',
            'lang': 'zh-tw',
            'routeType': '2',
            'device': 'web'
        },
        'file_path': 'D:/School/MPU_Master/BusData/get_weather/grandprix/arrival_records_26_grandprix.csv'
    },
    {
        'route_name': '73',
        'bus_url': 'https://bis.dsat.gov.mo:37812/macauweb/routestation/bus',
        'traffic_url': 'https://bis.dsat.gov.mo:37812/ddbus/common/supermap/routeStation/traffic?device=web&HUID=fd7444de-b635-400d-bf59-b0793114ebc4&routeCode=00073&direction=0&indexType=00&lang=zh_tw&categoryIds=BCAFBD938B8D48B0B3F598B44DD32E6C',
        'request_param': {
            'action': 'dy',
            'routeName': '73',
            'dir': '0',
            'lang': 'zh-tw',
            'routeType': '2',
            'device': 'web'
        },
        'file_path': 'D:/School/MPU_Master/BusData/get_weather/grandprix/arrival_records_73_grandprix.csv'
    },
    {
        'route_name': 'AP1',
        'bus_url': 'https://bis.dsat.gov.mo:37812/macauweb/routestation/bus',
        'traffic_url': 'https://bis.dsat.gov.mo:37812/ddbus/common/supermap/routeStation/traffic?device=web&HUID=fd7444de-b635-400d-bf59-b0793114ebc4&routeCode=00AP1&direction=0&indexType=00&lang=zh_tw&categoryIds=BCAFBD938B8D48B0B3F598B44DD32E6C',
        'request_param': {
            'action': 'dy',
            'routeName': 'AP1',
            'dir': '0',
            'lang': 'zh-tw',
            'routeType': '2',
            'device': 'web'
        },
        'file_path': 'D:/School/MPU_Master/BusData/get_weather/grandprix/arrival_records_AP1_grandprix.csv'
    }
]

def main():
    """Main function - run five route crawlers simultaneously"""
    logging.info("Starting fixed version of five-route bus data collection system")
    
    # Create weather monitor instance
    weather_api_key = "5796abbde9106b7da4febfae8c44c232"  # Weather API key
    weather_monitor = WeatherMonitor(weather_api_key)
    
    # Wait for weather monitor initialization
    time.sleep(5)
    
    # Create crawler instances
    crawlers = []
    threads = []
    
    for config in ROUTE_CONFIGS:
        crawler = FixedBusRouteCrawler(config, weather_monitor)
        crawlers.append(crawler)
        
        # Create thread for each crawler
        thread = threading.Thread(target=crawler.run)
        thread.daemon = True
        threads.append(thread)
    
    # Start all threads
    for i, thread in enumerate(threads):
        thread.start()
        logging.info(f"Started route {ROUTE_CONFIGS[i]['route_name']} monitoring thread")
        time.sleep(3)  # Stagger startup times to avoid simultaneous requests
    
    try:
        # Wait for all threads to complete (will actually run until interrupted)
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        logging.info("Received interrupt signal, stopping all crawlers")
    except Exception as e:
        logging.error(f"System runtime error: {e}")

if __name__ == "__main__":
    main()