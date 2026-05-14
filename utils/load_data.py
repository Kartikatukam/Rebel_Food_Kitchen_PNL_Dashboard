import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df = pd.read_csv(
        "C:\Project\Kitchen_PNL_Dashboard\data\Kittchen PNL Data.xlsx - Sheet 1 - stores.csv"
    )

    return df

