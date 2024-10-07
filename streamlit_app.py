import streamlit as st
import pandas as pd
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")




# (1) Add a drop-down for Category selection
selected_category = st.selectbox("Select a Category", df["Category"].unique())

# (2) Add a multi-select for Sub_Category based on selected Category
filtered_df = df[df["Category"] == selected_category]
selected_sub_categories = st.multiselect("Select Sub-Categories", filtered_df["Sub_Category"].unique())

# Filter dataframe by selected sub-categories
if selected_sub_categories:
    filtered_df = filtered_df[filtered_df["Sub_Category"].isin(selected_sub_categories)]

# (3) Show a line chart of sales for the selected items
sales_chart = filtered_df.groupby('Order_Date')['Sales'].sum().reset_index()
    st.line_chart(sales_chart, x='Order_Date', y='Sales')

# (4) Calculate metrics for total sales, total profit, and overall profit margin (%)
if not filtered_df.empty:
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    # Calculate overall profit margin for all products across all categories (for delta comparison)
    all_products_sales = df["Sales"].sum()
    all_products_profit = df["Profit"].sum()
    overall_average_profit_margin = (all_products_profit / all_products_sales) * 100 if all_products_sales != 0 else 0
    delta_margin = overall_profit_margin - overall_average_profit_margin

    # Display metrics using Streamlit's `st.metric` function
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Overall Profit Margin", value=f"{overall_profit_margin:.2f}%", delta=f"{delta_margin:.2f}%")

