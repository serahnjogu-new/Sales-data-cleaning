import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuration
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 3, 31)
DATE_RANGE = pd.date_range(start=START_DATE, end=END_DATE, freq='h') # Hourly data
NUM_SENSORS = 5
NUM_VEHICLES = 20

def generate_weather(date_range):
    """Generates hourly weather data."""
    print("Generating Weather Data...")
    n = len(date_range)
    temps = []
    rainfall = []
    conditions = []
    
    for date in date_range:
        # Simple seasonal adjustment
        base_temp = 15 if date.month in [12, 1, 2] else 25
        # Daily cycle
        daily_fluc = -5 if date.hour < 6 or date.hour > 20 else 5
        
        temp = base_temp + daily_fluc + np.random.normal(0, 3)
        temps.append(round(temp, 1))
        
        # Random rain
        if np.random.random() < 0.1: # 10% chance of rain
            rain_mm = round(np.random.exponential(2), 1)
            condition = "Rainy" if rain_mm > 0.5 else "Cloudy"
        else:
            rain_mm = 0.0
            condition = "Clear"
            
        rainfall.append(rain_mm)
        conditions.append(condition)
        
    df = pd.DataFrame({
        'Timestamp': date_range,
        'Temperature': temps,
        'Rainfall_mm': rainfall,
        'Weather_Condition': conditions
    })
    df.to_csv('weather_data.csv', index=False)
    print("Saved weather_data.csv")
    return df

def generate_events(start_date, end_date):
    """Generates a random event schedule."""
    print("Generating Event Schedule...")
    current = start_date
    events = []
    event_types = ['Concert', 'Sports Game', 'Festival', 'Public Holiday', 'Protest']
    
    while current <= end_date:
        if np.random.random() < 0.1: # 10% chance of an event on a given day
            event_name = random.choice(event_types)
            location = f"Zone_{random.randint(1, NUM_SENSORS)}"
            events.append({
                'Date': current.date(),
                'Event_Name': event_name,
                'Location': location,
                'Attendance': random.randint(1000, 50000)
            })
        current += timedelta(days=1)
        
    df = pd.DataFrame(events)
    df.to_csv('event_schedule.csv', index=False)
    print("Saved event_schedule.csv")
    return df

def generate_sensor_data(date_range):
    """Generates hourly traffic counts for sensors."""
    print("Generating Sensor Data...")
    
    data = []
    for sensor_id in range(1, NUM_SENSORS + 1):
        for ts in date_range:
            # Base traffic pattern: Peaks at 8AM and 5PM
            hour = ts.hour
            if 7 <= hour <= 9 or 16 <= hour <= 18:
                base_count = 500 # Rush hour
            elif 10 <= hour <= 15:
                base_count = 300 # Mid-day
            else:
                base_count = 50 # Night
                
            # Randomness
            count = int(np.random.normal(base_count, 50))
            count = max(0, count) # No negative cars
            
            data.append({
                'Timestamp': ts,
                'Sensor_ID': f"Sensor_{sensor_id}",
                'Vehicle_Count': count
            })
            
    df = pd.DataFrame(data)
    df.to_csv('traffic_sensors.csv', index=False)
    print("Saved traffic_sensors.csv")
    return df

def generate_gps_data(date_range):
    """Generates a subset of vehicle traces."""
    print("Generating GPS Data (Sample)...")
    # GPS data is huge, so we'll just generate sparse checks for a few vehicles
    
    gps_logs = []
    
    # Random timestamps subset (every 4 hours to save space)
    sample_times = date_range[::4] 
    
    for vehicle_id in range(1, NUM_VEHICLES + 1):
        # Assign a 'home' zone
        lat_base = 40.7128 + np.random.normal(0, 0.05)
        lon_base = -74.0060 + np.random.normal(0, 0.05)
        
        for ts in sample_times:
            # Move slightly
            lat = lat_base + np.random.normal(0, 0.01)
            lon = lon_base + np.random.normal(0, 0.01)
            speed = np.random.randint(0, 80) # km/h
            
            gps_logs.append({
                'Timestamp': ts,
                'Vehicle_ID': f"V{vehicle_id}",
                'Latitude': lat,
                'Longitude': lon,
                'Speed_kmh': speed
            })
            
    df = pd.DataFrame(gps_logs)
    df.to_csv('gps_data.csv', index=False)
    print("Saved gps_data.csv")
    return df

if __name__ == "__main__":
    w_df = generate_weather(DATE_RANGE)
    e_df = generate_events(START_DATE, END_DATE)
    s_df = generate_sensor_data(DATE_RANGE)
    g_df = generate_gps_data(DATE_RANGE)
    print("Data Generation Complete.")
