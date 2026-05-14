
import streamlit as st
import pandas as pd

from utils.load_data import load_data


def show_variance_dashboard():

    st.title("Variance Level PNL Dashboard")

    df = load_data()

    df["VARIANCE %"] = (
        df["VARIANCE"] / df["NET REVENUE"]
    ) * 100

    def variance_bucket(x):

        if x < 2:
            return "Var <2%"

        elif x < 3:
            return "Var 2% to 3%"

        elif x < 5:
            return "Var 3% to 5%"

        else:
            return "Var >5%"

    df["VARIANCE CATEGORY"] = df[
        "VARIANCE %"
    ].apply(variance_bucket)


    # Filters (Sider bar)
    variance_filter = st.sidebar.multiselect(
        "Variance Category",
        df["VARIANCE CATEGORY"].unique()
    )

    revenue_filter = st.sidebar.multiselect(
        "Revenue Cohort",
        df["REVENUE COHORT"].unique()
    )

    city_filter = st.sidebar.multiselect(
        "City",
        df["CITY"].unique()
    )

    month_filter = st.sidebar.multiselect(
        "Month",
        df["MONTH"].unique()
    )

    revenue_range = st.sidebar.slider(
        "Revenue Range",
        int(df["NET REVENUE"].min()),
        int(df["NET REVENUE"].max()),
        (
            int(df["NET REVENUE"].min()),
            int(df["NET REVENUE"].max())
        )
    )


    # Filters conditions
    filtered_df = df.copy()

    if variance_filter:
        filtered_df = filtered_df[
            filtered_df["VARIANCE CATEGORY"].isin(
                variance_filter
            )
        ]

    if revenue_filter:
        filtered_df = filtered_df[
            filtered_df["REVENUE COHORT"].isin(
                revenue_filter
            )
        ]

    if city_filter:
        filtered_df = filtered_df[
            filtered_df["CITY"].isin(city_filter)
        ]

    if month_filter:
        filtered_df = filtered_df[
            filtered_df["MONTH"].isin(month_filter)
        ]


    month_order = [
        "Oct-23",
        "Nov-23",
        "Dec-23",
        "Jan-24",
        "Feb-24",
        "Mar-24"
    ]

    filtered_df["MONTH"] = pd.Categorical(
        filtered_df["MONTH"],
        categories=month_order,
        ordered=True
    )

    filtered_df = filtered_df[
        (filtered_df["NET REVENUE"] >= revenue_range[0]) &
        (filtered_df["NET REVENUE"] <= revenue_range[1])
        ]


    # SUB-DASHBOARD 1 AVG VARIANCE % -----
    st.subheader(
        "Variance by Revenue Category (%)"
    )

    variance_summary = pd.pivot_table(
        filtered_df,
        values="VARIANCE %",
        index="REVENUE COHORT",
        columns="MONTH",
        aggfunc="mean"
    )

    variance_summary = variance_summary.round(2)

    st.dataframe(
        variance_summary,
        use_container_width=True
    )

    # SUB-DASHBOARD 2  STORE COUNT -----
    st.subheader(
        "Store Count by Revenue Category"
    )

    store_summary = pd.pivot_table(
        filtered_df,
        values="STORE",
        index="REVENUE COHORT",
        columns="MONTH",
        aggfunc="nunique"
    )

    st.dataframe(
        store_summary,
        use_container_width=True
    )

    st.subheader("Variance Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
