import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import process_traffic_data, validate_data
from utils.visualizations import (
    create_traffic_flow_chart,
    create_hourly_pattern_chart,
    create_traffic_map,
    create_vehicle_distribution_chart
)
from data.sample_traffic_data import get_sample_data

# Page configuration
st.set_page_config(
    page_title="Traffic Analysis Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Title and description
st.title("🚗 Traffic Analysis Dashboard")
st.markdown("""
    Analyze and visualize traffic patterns with this interactive dashboard.
    Upload your traffic data or use sample data to get started.
""")

# Sidebar
st.sidebar.title("Controls")
data_source = st.sidebar.radio(
    "Select Data Source",
    ["Upload Data", "Use Sample Data"]
)

# Initialize processed_df as None to check if it's defined later
processed_df = None

# Data loading
if data_source == "Upload Data":
    uploaded_file = st.sidebar.file_uploader(
        "Upload Traffic Data (CSV)",
        type=['csv'],
        help="Upload a CSV file with columns: timestamp, vehicle_count, location_lat, location_lon, vehicle_type"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if validate_data(df):
                processed_df = process_traffic_data(df)
            else:
                st.error("Invalid data format. Please check the required columns.")
                st.stop()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.stop()
    else:
        st.info("Please upload a CSV file or use sample data.")
        # Changed: Don't stop execution here, allow showing the UI with a message
        # Instead, we'll check if processed_df exists before using it
else:
    df = get_sample_data()
    processed_df = process_traffic_data(df)

# Only show filters and visualizations if we have data
if processed_df is not None:
    # Filters
    st.sidebar.subheader("Filters")
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(processed_df['timestamp'].min().date(), processed_df['timestamp'].max().date())
    )

    selected_vehicle_types = st.sidebar.multiselect(
        "Vehicle Types",
        options=processed_df['vehicle_type'].unique(),
        default=processed_df['vehicle_type'].unique()
    )

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Traffic Flow Over Time")
        traffic_flow_chart = create_traffic_flow_chart(processed_df, date_range, selected_vehicle_types)
        st.plotly_chart(traffic_flow_chart, use_container_width=True)

    with col2:
        st.subheader("Hourly Traffic Pattern")
        hourly_pattern_chart = create_hourly_pattern_chart(processed_df, selected_vehicle_types)
        st.plotly_chart(hourly_pattern_chart, use_container_width=True)

    # Map visualization
    st.subheader("Traffic Distribution Map")
    traffic_map = create_traffic_map(processed_df)
    st.components.v1.html(traffic_map._repr_html_(), height=400)

    # Vehicle distribution
    st.subheader("Vehicle Type Distribution")
    vehicle_dist_chart = create_vehicle_distribution_chart(processed_df)
    st.plotly_chart(vehicle_dist_chart, use_container_width=True)

    # Export functionality
    st.sidebar.subheader("Export Data")
    if st.sidebar.button("Export Processed Data"):
        csv = processed_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name="processed_traffic_data.csv",
            mime="text/csv"
        )
else:
    # Display a message if no data is loaded yet
    st.markdown("### Please upload data or select 'Use Sample Data' to view the dashboard.")