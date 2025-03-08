import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def validate_data(df):
    """Validate if the dataframe has required columns."""
    required_columns = ['timestamp', 'vehicle_count', 'location_lat', 'location_lon', 'vehicle_type']
    return all(column in df.columns for column in required_columns)

def process_traffic_data(df):
    """Process raw traffic data for analysis."""
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort by timestamp
    df = df.sort_values('timestamp')
    
    # Calculate hourly aggregates
    df['hour'] = df['timestamp'].dt.hour
    df['date'] = df['timestamp'].dt.date
    
    # Calculate moving averages
    df['moving_avg_count'] = df.groupby('vehicle_type')['vehicle_count'].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )
    
    # Calculate peak hours
    hourly_counts = df.groupby(['hour', 'vehicle_type'])['vehicle_count'].mean().reset_index()
    df['is_peak_hour'] = df.apply(
        lambda x: hourly_counts[
            (hourly_counts['hour'] == x['hour']) & 
            (hourly_counts['vehicle_type'] == x['vehicle_type'])
        ]['vehicle_count'].iloc[0] > hourly_counts['vehicle_count'].mean(),
        axis=1
    )
    
    return df