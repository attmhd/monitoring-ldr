import streamlit as st
import pandas as pd
import requests
import plotly.express as px


# Utility function to fetch data from the API
def fetch_ldr_data(api_url="http://127.0.0.1:8000/get_data"):
    """Fetch LDR data from the API."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Will raise an exception for 4xx or 5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None


# Utility function to process data and ensure the necessary columns exist
def process_data(data):
    """Process the raw API data into a DataFrame."""
    if data and "result" in data:
        df = pd.DataFrame(data["result"])
        if {"ldr_value", "timestamp"}.issubset(df.columns):
            df["Timestamp"] = pd.to_datetime(df["timestamp"])
            df = df[["ldr_value", "Timestamp"]].rename(columns={"ldr_value": "LDR Value", "Timestamp": "Timestamp"})
            return df
    return None


# Function to display data table
def display_data_table(df):
    """Display the data table."""
    if df is not None:
        st.subheader("LDR Data Table")
        st.dataframe(df, width=700)
    else:
        st.warning("No valid data available to display.")


# Function to display the latest LDR value
def display_latest_ldr_value(df):
    """Display the latest LDR value as a metric."""
    if df is not None and not df.empty:
        latest_row = df.iloc[-1]
        st.metric("Latest LDR Value", f"{latest_row['LDR Value']:.2f} Volt", f"Recorded at {latest_row['Timestamp']}")
    else:
        st.warning("No valid data available for latest LDR value.")


# Function to display a line chart for LDR data
def display_line_chart(df):
    """Display a line chart for LDR values over time."""
    if df is not None and not df.empty:
        fig = px.line(df, x="Timestamp", y="LDR Value")
        fig.update_yaxes(range=[0, 3.3], title_text='LDR Value (V)')
        fig.update_xaxes(title_text='Timestamp')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valid data available for the chart.")


# Main function to handle the app logic
def main():
    st.set_page_config(layout="wide", page_title="LDR Monitoring")
    st.title("Monitoring LDR Data")

    # Fetch and process data
    data = fetch_ldr_data()
    df = process_data(data)

    # Layout: Display the latest LDR value, data table, and line chart
    if df is not None:
        col1, col2 = st.columns(2)
        with col1:
            display_latest_ldr_value(df)

        with col2:
            display_data_table(df)

        st.subheader("LDR Value Over Time")
        display_line_chart(df)
    else:
        st.warning("Unable to fetch or process the LDR data.")


if __name__ == '__main__':
    main()
