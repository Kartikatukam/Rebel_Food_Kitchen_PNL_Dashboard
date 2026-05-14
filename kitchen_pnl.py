import streamlit as st
import plotly.express as px
import pandas as pd

from utils.load_data import load_data


def show_kitchen_dashboard():

    st.title("Kitchen Level PNL Dashboard")

    df = load_data()


# Sidebar filter
    month = st.sidebar.multiselect(
        "Select Month",
        df["MONTH"].unique()
    )

    city = st.sidebar.multiselect(
        "Select City",
        df["CITY"].unique()
    )

    store = st.sidebar.multiselect(
        "Select Store",
        df["STORE"].unique()
    )

    ebitda_range = st.sidebar.slider(
        "Select EBITDA Range",
        int(df["KITCHEN EBITDA"].min()),
        int(df["KITCHEN EBITDA"].max()),
        (
            int(df["KITCHEN EBITDA"].min()),
            int(df["KITCHEN EBITDA"].max())
        )
    )


    revenue_range = st.sidebar.slider(
        "Select Revenue Range",
        int(df["NET REVENUE"].min()),
        int(df["NET REVENUE"].max()),
        (
            int(df["NET REVENUE"].min()),
            int(df["NET REVENUE"].max()),
        )
    )


    # Advance filter (on dashboard part)


    st.subheader("Advanced Filters")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        revenue_cohort = st.multiselect(
            "Revenue Cohort",
            df["REVENUE COHORT"].unique()
        )

        ebitda_category = st.multiselect(
            "EBITDA Category",
            df["EBITDA CATEGORY"].unique()
        )

        gm_range = st.slider(
            "GM % Range",
            float(df["GM%"].min()),
            float(df["GM%"].max()),
            (
                float(df["GM%"].min()),
                float(df["GM%"].max())
            )
        )

    with filter_col2:

        zone = st.multiselect(
            "Zone",
            df["ZONE MAPPING"].unique()
        )

        cm_cohort = st.multiselect(
            "CM Cohort",
            df["CM COHORT"].unique()
        )

        ebitda_cohort = st.multiselect(
            "EBITDA Cohort",
            df["EBITDA COHORT"].unique()
        )


# Filtering condition
    filtered_df = df.copy()

    if month:
        filtered_df = filtered_df[
            filtered_df["MONTH"].isin(month)
        ]

    if city:
        filtered_df = filtered_df[
            filtered_df["CITY"].isin(city)
        ]

    if store:
        filtered_df = filtered_df[
            filtered_df["STORE"].isin(store)
        ]

    if revenue_cohort:
        filtered_df = filtered_df[
            filtered_df["REVENUE COHORT"].isin(revenue_cohort)
        ]

    if ebitda_category:
        filtered_df = filtered_df[
            filtered_df["EBITDA CATEGORY"].isin(ebitda_category)
        ]

    if zone:
        filtered_df = filtered_df[
            filtered_df["ZONE MAPPING"].isin(zone)
        ]

    if cm_cohort:
        filtered_df = filtered_df[
            filtered_df["CM COHORT"].isin(cm_cohort)
        ]

    if ebitda_cohort:
        filtered_df = filtered_df[
            filtered_df["EBITDA COHORT"].isin(ebitda_cohort)
        ]

    filtered_df = filtered_df[
        (filtered_df["KITCHEN EBITDA"] >= ebitda_range[0]) &
        (filtered_df["KITCHEN EBITDA"] <= ebitda_range[1])
    ]

    filtered_df = filtered_df[
        (filtered_df["NET REVENUE"] >= revenue_range[0]) &
        (filtered_df["NET REVENUE"] <= revenue_range[1])
        ]

    filtered_df = filtered_df[
        (filtered_df["GM%"] >= gm_range[0]) &
        (filtered_df["GM%"] <= gm_range[1])
    ]


# KPI's section

    total_revenue = filtered_df["NET REVENUE"].sum()

    total_orders = filtered_df["ORDER COUNT"].sum()

    total_store = filtered_df["STORE"].nunique()

    avg_discount = filtered_df["DISCOUNT"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"₹ {total_revenue:,.0f}"
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Total Store",
        f"{total_store}"
    )

    col4.metric(
        "Avg Discount",
        f"₹ {avg_discount:,.0f}"
    )

    month_order = [
        "Oct-23",
        "Nov-23",
        "Dec-23",
        "Jan-24",
        "Feb-24",
        "Mar-24"
    ]


    revenue_by_city = filtered_df.groupby(
        "CITY"
    )["NET REVENUE"].sum().reset_index()

    fig = px.bar(
        revenue_by_city,
        x="CITY",
        y="NET REVENUE",
        title="Revenue by City",
        color_discrete_sequence=["#66b3ff"]
    )


    revenue_by_month = filtered_df.groupby(
        "MONTH"
    )["NET REVENUE"].sum().reset_index()

    revenue_by_month["MONTH"] = pd.Categorical(
        revenue_by_month["MONTH"],
        categories=month_order,
        ordered=True
    )

    revenue_by_month = revenue_by_month.sort_values("MONTH")

    fig1 = px.line(
        revenue_by_month,
        x="MONTH",
        y="NET REVENUE",
        title="Revenue Trend by Month",
        markers=True
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with chart_col2:
        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    gm_by_month = filtered_df.groupby(
        "MONTH"
    )["GROSS MARGIN"].mean().reset_index()

    gm_by_month["MONTH"] = pd.Categorical(
        gm_by_month["MONTH"],
        categories=month_order,
        ordered=True
    )

    gm_by_month = gm_by_month.sort_values("MONTH")

    fig5 = px.line(
        gm_by_month,
        x="MONTH",
        y="GROSS MARGIN",
        title="Average Gross Margin Trend",
        markers=True
    )

    st.plotly_chart(
        fig5,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.dataframe(filtered_df)

    st.subheader("Key Business Insights")

    st.markdown("""
    - Stores with higher revenue generally performed better in terms of EBITDA, showing that larger kitchens were more profitable overall.
    
    - Revenue improved noticeably after Jan-24, which suggests stronger business performance and increased customer demand in later months.

    - A few stores generated high revenue but still had lower Gross Margins, which may indicate higher operating or food costs.

    - Smaller revenue cohorts showed relatively higher variance levels, pointing towards possible wastage or inventory management issues.

    - Revenue contribution was mainly driven by a few major cities, while smaller cities contributed less to the overall business revenue.

    - Gross Margin trends remained fairly stable across months, indicating consistent pricing and operational performance.

    - The dashboard filters helped identify how profitability and variance changed across different cities, stores, and revenue categories.
    """)