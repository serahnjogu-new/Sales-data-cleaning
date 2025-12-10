import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def load_data():
    """Loads raw datasets."""
    print("Loading data...")
    sensors = pd.read_csv('traffic_sensors.csv', parse_dates=['Timestamp'])
    weather = pd.read_csv('weather_data.csv', parse_dates=['Timestamp'])
    gps = pd.read_csv('gps_data.csv', parse_dates=['Timestamp'])
    events = pd.read_csv('event_schedule.csv', parse_dates=['Date'])
    return sensors, weather, gps, events

def process_data(sensors, weather, gps, events):
    """Merges and processes the data."""
    print("Processing data...")
    
    # 1. Aggregate GPS Speed (Avg speed per hour)
    # We round GPS timestamp to nearest hour to match sensors
    gps['HourBucket'] = gps['Timestamp'].dt.floor('h')
    avg_speed = gps.groupby('HourBucket')['Speed_kmh'].mean().reset_index()
    avg_speed.rename(columns={'HourBucket': 'Timestamp', 'Speed_kmh': 'Avg_GPS_Speed'}, inplace=True)
    
    # 2. Merge Sensors + Weather + Aggregated GPS
    df = pd.merge(sensors, weather, on='Timestamp', how='left')
    df = pd.merge(df, avg_speed, on='Timestamp', how='left')
    
    # Fill missing GPS speeds (if no cars were tracked that hour) with global mean
    df['Avg_GPS_Speed'] = df['Avg_GPS_Speed'].fillna(df['Avg_GPS_Speed'].mean())
    
    # 3. Merge Events
    # Create a Date column for merging
    df['Date'] = df['Timestamp'].dt.date
    # Events 'Date' is datetime, convert to date object for merge
    events['Date'] = events['Date'].dt.date
    
    df = pd.merge(df, events, on='Date', how='left')
    
    # Fill missing events with "None"
    df['Event_Name'] = df['Event_Name'].fillna('No Event')
    df['Attendance'] = df['Attendance'].fillna(0)
    df.drop(columns=['Location', 'Date'], inplace=True) # Drop helpers/redundant
    
    # 4. Feature Engineering
    df['Hour'] = df['Timestamp'].dt.hour
    df['DayOfWeek'] = df['Timestamp'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    
    # 5. One Hot Encoding for Categorical
    # Sensor_ID, Weather_Condition, Event_Name
    # We will use pandas get_dummies for simplicity in this script
    df = pd.get_dummies(df, columns=['Sensor_ID', 'Weather_Condition', 'Event_Name'], drop_first=True)
    
    # 6. Normalization (numerical features)
    # Target variable 'Vehicle_Count' should generally NOT be scaled if we want interpretable RMSE,
    # but for some models it helps. We'll scale inputs but keep target raw for now.
    features_to_scale = ['Temperature', 'Rainfall_mm', 'Avg_GPS_Speed', 'Attendance']
    scaler = StandardScaler()
    df[features_to_scale] = scaler.fit_transform(df[features_to_scale])
    
    print(f"Processed dataframe shape: {df.shape}")
    df.to_csv('processed_data.csv', index=False)
    print("Saved processed_data.csv")
    return df

if __name__ == "__main__":
    sensors, weather, gps, events = load_data()
    df = process_data(sensors, weather, gps, events)
