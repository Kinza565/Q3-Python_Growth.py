import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for Dark Theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("Data Sweeper Sterling Integrator by Kinza Khan")
st.markdown("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. This project is created for Quarter 3!")

# File Upload
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Unsupported file format: {file_ext}. Please upload a CSV or Excel file.")
                continue

            # File Preview
            st.subheader(f"Preview of {file.name}")
            st.dataframe(df.head())

            # Data Cleaning Options
            st.subheader(f"Data Cleaning Options for {file.name}")
            if st.checkbox(f"Clean data for {file.name}"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Remove Duplicates"):
                        df.drop_duplicates(inplace=True)
                        st.success("Duplicates removed successfully.")

                with col2:
                    if st.button("Fill Missing Numeric Values"):
                        numeric_cols = df.select_dtypes(include=["number"]).columns
                        df[numeric_cols] = df[numeric_cols].apply(lambda x: x.fillna(x.median()))
                        st.success("Missing numeric values filled with median.")

                selected_columns = st.multiselect("Select Columns to Keep:", df.columns, default=df.columns)
                if selected_columns:
                    df = df[selected_columns]

            # Data Visualization
            st.subheader("Data Visualization")
            if st.checkbox(f"Show Visualizations for {file.name}"):
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            # Conversion Options
            st.subheader("File Conversion")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_ext = ".csv"
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    file_ext = ".xlsx"
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                
                st.download_button(
                    label=f"Download {file.name.replace(file_ext, conversion_type.lower())}",
                    data=buffer,
                    file_name=f"{file.name.replace(file_ext, conversion_type.lower())}",
                    mime=mime_type
                )
                st.success("File processed and ready for download!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.sidebar.title("✨ About the App")
st.sidebar.info("This Data Sweeper App is developed by Kinza Khan to automate file transformation, data cleaning, and visualization.")

st.sidebar.write("🔑 Version: 1.0")
st.sidebar.write("💪 Powered by Streamlit")
