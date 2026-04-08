import streamlit as st
import pandas as pd
import datetime

st.title("🚀 Professional Data Cleaner")
st.write("Upload your messy CSV, and I'll return a production-ready file.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the data
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # --- THE CLEANING ENGINE ---
    # Fix numbers
    if 'Amount' in df.columns:
        df['Amount'] = df['Amount'].fillna(df['Amount'].median())
    
    # Fix dates
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Date'] = df['Date'].fillna(pd.Timestamp.now().normalize())
    
    # Fix text
    if 'Vendor' in df.columns:
        df['Vendor'] = df['Vendor'].fillna('UNKNOWN')

    # Add audit trail
    df['Processed_At'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.subheader("Cleaned Data Preview")
    st.dataframe(df.head())

    # --- DOWNLOAD BUTTON ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv",
    )
