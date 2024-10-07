import streamlit as st
import pandas as pd

# Load the data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)

# Ensure 'Order Date' is in datetime format
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Set up the title
st.title("Data App Assignment")

# (1) Dropdown for Category
categories = df["Category"].unique()
selected_category = st.selectbox("Select Category", categories)

# Filter by selected category
filtered_df = df[df["Category"] == selected_category]

# (2) Multi-select for Sub-Category based on selected Category
subcategories = filtered_df["Sub-Category"].unique()
selected_subcategories = st.multiselect("Select Sub-Category", subcategories)

# Filter by selected subcategories
if selected_subcategories:
    filtered_df = filtered_df[filtered_df["Sub-Category"].isin(selected_subcategories)]

# (3) Line chart for sales of the selected items
if not filtered_df.empty:
    sales_by_date = filtered_df.groupby(pd.Grouper(key='Order_Date', freq='M')).sum()
    st.line_chart(sales_by_date['Sales'])

# (4) Show metrics for total sales, total profit, and overall profit margin for the selected items
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# (5) Calculate the overall average profit margin for all products
overall_total_sales = df["Sales"].sum()
overall_total_profit = df["Profit"].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales != 0 else 0
delta_profit_margin = profit_margin - overall_profit_margin

# Display metrics with delta
st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Profit Margin (%)", value=f"{profit_margin:.2f}%", delta=f"{delta_profit_margin:.2f}%")

# Show data table
st.write("### Filtered Data")
st.dataframe(filtered_df)
