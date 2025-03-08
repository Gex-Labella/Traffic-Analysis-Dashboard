import plotly.express as px
import plotly.graph_objects as go
import folium
from folium import plugins
import pandas as pd

def create_traffic_flow_chart(df, date_range, vehicle_types):
    """Create an interactive traffic flow visualization."""
    filtered_df = df[
        (df['date'] >= date_range[0]) & 
        (df['date'] <= date_range[1]) &
        (df['vehicle_type'].isin(vehicle_types))
    ]
    
    fig = px.line(
        filtered_df,
        x='timestamp',
        y='vehicle_count',
        color='vehicle_type',
        line_group='vehicle_type',
        title='Traffic Flow Over Time'
    )
    
    fig.add_traces(
        px.line(
            filtered_df,
            x='timestamp',
            y='moving_avg_count',
            color='vehicle_type',
            line_dash='vehicle_type'
        ).data
    )
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Vehicle Count",
        hovermode='x unified'
    )
    
    return fig

def create_hourly_pattern_chart(df, vehicle_types):
    """Create hourly traffic pattern visualization."""
    hourly_data = df[df['vehicle_type'].isin(vehicle_types)].groupby(
        ['hour', 'vehicle_type']
    )['vehicle_count'].mean().reset_index()
    
    fig = px.line(
        hourly_data,
        x='hour',
        y='vehicle_count',
        color='vehicle_type',
        title='Average Hourly Traffic Pattern'
    )
    
    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Average Vehicle Count",
        xaxis=dict(tickmode='linear', tick0=0, dtick=1)
    )
    
    return fig

def create_traffic_map(df):
    """Create a map visualization of traffic data."""
    center_lat = df['location_lat'].mean()
    center_lon = df['location_lon'].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='cartodbpositron'
    )
    
    # Add heatmap
    heat_data = df[['location_lat', 'location_lon', 'vehicle_count']].values.tolist()
    plugins.HeatMap(heat_data).add_to(m)
    
    return m

def create_vehicle_distribution_chart(df):
    """Create vehicle type distribution visualization."""
    vehicle_dist = df.groupby('vehicle_type')['vehicle_count'].sum().reset_index()
    
    fig = px.pie(
        vehicle_dist,
        values='vehicle_count',
        names='vehicle_type',
        title='Vehicle Type Distribution'
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig