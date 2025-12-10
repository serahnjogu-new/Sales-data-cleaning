import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_raw_data_for_viz():
    # Load raw for easier categorical plotting
    sensors = pd.read_csv('traffic_sensors.csv', parse_dates=['Timestamp'])
    weather = pd.read_csv('weather_data.csv', parse_dates=['Timestamp'])
    
    # Merge for analysis
    df = pd.merge(sensors, weather, on='Timestamp', how='left')
    df['Hour'] = df['Timestamp'].dt.hour
    return df

def plot_traffic_by_hour(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Hour', y='Vehicle_Count', estimator='mean', errorbar='sd')
    plt.title('Average Traffic Volume by Hour of Day')
    plt.xlabel('Hour (0-23)')
    plt.ylabel('Vehicle Count')
    plt.grid(True)
    plt.savefig('traffic_by_hour.png')
    print("Saved traffic_by_hour.png")

def plot_traffic_by_weather(df):
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='Weather_Condition', y='Vehicle_Count')
    plt.title('Traffic Volume Distribution by Weather Condition')
    plt.savefig('traffic_by_weather.png')
    print("Saved traffic_by_weather.png")
    
def plot_heatmap(df):
    plt.figure(figsize=(8, 6))
    # Select numeric columns
    numeric_df = df[['Vehicle_Count', 'Temperature', 'Rainfall_mm', 'Hour']]
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.savefig('traffic_heatmap.png')
    print("Saved traffic_heatmap.png")

if __name__ == "__main__":
    df = load_raw_data_for_viz()
    plot_traffic_by_hour(df)
    plot_traffic_by_weather(df)
    plot_heatmap(df)
