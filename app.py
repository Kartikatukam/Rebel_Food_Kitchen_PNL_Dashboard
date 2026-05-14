import streamlit as st


from kitchen_pnl import show_kitchen_dashboard
from variance_pnl import show_variance_dashboard

st.set_page_config(
    page_title="Kitchen Dashboard",
    layout= "wide"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to", ["Kitchen PNL",
            "Variance PNL" ]
)

if page == "Kitchen PNL":
    show_kitchen_dashboard()
elif page == "Variance PNL":
    show_variance_dashboard()
