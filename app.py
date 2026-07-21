import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="BrightMart Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 BrightMart Sales Analytics Dashboard")
st.markdown("Analyze sales performance across customers, products and regions.")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():

    customers = pd.read_csv("customers.csv")
    products = pd.read_csv("products.csv")
    orders = pd.read_csv("orders.csv")
    order_items = pd.read_csv("order_items.csv")

    orders["order_date"] = pd.to_datetime(orders["order_date"])
    customers["signup_date"] = pd.to_datetime(customers["signup_date"])

    df = order_items.merge(
        orders,
        on="order_id",
        how="left"
    )

    df = df.merge(
        customers,
        on="customer_id",
        how="left"
    )

    df_master = df.merge(
        products,
        on="product_id",
        how="left"
    )

    df_master["line_revenue"] = (
        df_master["quantity"]
        * df_master["unit_price"]
        * (1 - df_master["discount"])
    )

    df_master["order_month"] = (
        df_master["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    df_active = df_master[
        df_master["order_status"] != "Cancelled"
    ]

    return df_master, df_active


# -----------------------------
# Load Master Data
# -----------------------------
df_master, df_active = load_data()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(
    ["📊 Dashboard", "👤 Customer Deep Dive"]
)

# =============================
# Dashboard Tab
# =============================
with tab1:

    st.sidebar.header("🔍 Filter Data")

    region = st.sidebar.multiselect(
        "Select Region",
        options=df_active["region"].unique(),
        default=df_active["region"].unique()
    )

    category = st.sidebar.multiselect(
        "Select Category",
        options=df_active["category"].unique(),
        default=df_active["category"].unique()
    )

    segment = st.sidebar.multiselect(
        "Select Segment",
        options=df_active["segment"].unique(),
        default=df_active["segment"].unique()
    )

    start_date = df_active["order_date"].min()
    end_date = df_active["order_date"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(start_date, end_date)
    )

    filtered_df = df_active[
        (df_active["region"].isin(region)) &
        (df_active["category"].isin(category)) &
        (df_active["segment"].isin(segment))
    ]

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["order_date"] >= pd.to_datetime(date_range[0])) &
            (filtered_df["order_date"] <= pd.to_datetime(date_range[1]))
        ]

    total_revenue = filtered_df["line_revenue"].sum()
    total_orders = filtered_df["order_id"].nunique()

    avg_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    unique_customers = filtered_df["customer_id"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

    col2.metric(
        "📦 Total Orders",
        total_orders
    )

    col3.metric(
        "💳 Avg Order Value",
        f"₹{avg_order_value:,.0f}"
    )

    col4.metric(
        "👥 Unique Customers",
        unique_customers
    )
        # =============================
    # Charts Row 1
    # =============================
    col1, col2 = st.columns(2)

    monthly_sales = (
        filtered_df.groupby("order_month", as_index=False)["line_revenue"]
        .sum()
    )

    fig1 = px.line(
        monthly_sales,
        x="order_month",
        y="line_revenue",
        title="Monthly Revenue Trend",
        markers=True
    )

    col1.plotly_chart(fig1, use_container_width=True)

    category_sales = (
        filtered_df.groupby("category", as_index=False)["line_revenue"]
        .sum()
    )

    fig2 = px.bar(
        category_sales,
        x="category",
        y="line_revenue",
        color="category",
        title="Revenue by Category"
    )

    col2.plotly_chart(fig2, use_container_width=True)

    # =============================
    # Charts Row 2
    # =============================
    col3, col4 = st.columns(2)

    top_customers = (
        filtered_df.groupby("customer_name", as_index=False)["line_revenue"]
        .sum()
        .sort_values(by="line_revenue", ascending=False)
        .head(10)
    )

    fig3 = px.bar(
        top_customers,
        x="line_revenue",
        y="customer_name",
        orientation="h",
        title="Top 10 Customers by Revenue"
    )

    col3.plotly_chart(fig3, use_container_width=True)

    region_sales = (
        filtered_df.groupby("region", as_index=False)["line_revenue"]
        .sum()
    )

    fig4 = px.pie(
        region_sales,
        names="region",
        values="line_revenue",
        hole=0.4,
        title="Revenue by Region"
    )

    col4.plotly_chart(fig4, use_container_width=True)

    # =============================
    # Filtered Data
    # =============================
    st.subheader("📋 Filtered Data")

    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )


# =============================
# Customer Deep Dive Tab
# =============================
with tab2:

    st.header("👤 Customer Deep Dive")

    customer = st.selectbox(
        "Select Customer",
        sorted(df_active["customer_name"].unique())
    )

    customer_df = df_active[
        df_active["customer_name"] == customer
    ]

    lifetime_value = customer_df["line_revenue"].sum()
    total_orders = customer_df["order_id"].nunique()
    products_purchased = customer_df["product_id"].nunique()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Lifetime Value",
        f"₹{lifetime_value:,.0f}"
    )

    c2.metric(
        "📦 Total Orders",
        total_orders
    )

    c3.metric(
        "🛍️ Products Purchased",
        products_purchased
    )

    st.subheader("Customer Order History")

    st.dataframe(
        customer_df,
        use_container_width=True
    )
    st.subheader("Average Order Value by Segment")

segment_aov = (
    filtered_df.groupby("segment")
    .agg(
        Revenue=("line_revenue", "sum"),
        Orders=("order_id", "nunique")
    )
)

segment_aov["Average_Order_Value"] = (
    segment_aov["Revenue"] / segment_aov["Orders"]
)

st.dataframe(segment_aov)