import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_sample_data():
    """Generate sample traffic data for demonstration."""
    # Generate timestamps for the last 24 hours
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    timestamps = pd.date_range(start_time, end_time, freq='5T')
    
    # Vehicle types
    vehicle_types = ['Car', 'Truck', 'Bus', 'Motorcycle']
    
    # Generate sample data
    data = []
    for ts in timestamps:
        for vt in vehicle_types:
            # Generate random vehicle count with realistic patterns
            hour = ts.hour
            base_count = 50 if (hour >= 8 and hour <= 10) or (hour >= 16 and hour <= 18) else 20
            count = int(np.random.normal(base_count, base_count/4))
            count = max(0, count)
            
            # Generate location with small random variations
            base_lat = 40.7128  # Example: New York City
            base_lon = -74.0060
            
            data.append({
                'timestamp': ts,
                'vehicle_type': vt,
                'vehicle_count': count,
                'location_lat': base_lat + np.random.normal(0, 0.01),
                'location_lon': base_lon + np.random.normal(0, 0.01)
            })
    
    return pd.DataFrame(data)