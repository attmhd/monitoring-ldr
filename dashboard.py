import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt


# Fungsi untuk mendapatkan data dari API
def get_ldr_data():
    try:
        response = requests.get("http://localhost:8000/get_data")  # Endpoint untuk mengambil data
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []

# Ambil data dari API
data = get_ldr_data()

# Konversi data JSON menjadi DataFrame
if data:
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Menampilkan data dalam bentuk tabel
    st.subheader("Sensor LDR Data")
    st.dataframe(df)
    
    # Statistik LDR
    st.subheader("LDR Statistics")
    st.write(f"Average LDR Value: {df['ldr_value'].mean():.2f}")
    st.write(f"Maximum LDR Value: {df['ldr_value'].max():.2f}")
    st.write(f"Minimum LDR Value: {df['ldr_value'].min():.2f}")
    
    # Membuat grafik garis untuk data LDR
    st.subheader("LDR Value Trend")
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'], df['ldr_value'], marker='o', color='b', label="LDR Value")
    ax.set_xlabel("Time")
    ax.set_ylabel("LDR Value")
    ax.set_title("LDR Sensor Value Over Time")
    ax.legend()
    st.pyplot(fig)

else:
    st.warning("No data available.")

