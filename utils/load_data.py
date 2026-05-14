import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/Kittchen PNL Data.xlsx - Sheet 1 - stores.csv"
    )

    return df

