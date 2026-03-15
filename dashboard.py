import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Superstore Sales Dashboard")

# Load Data
df = pd.read_csv("data/superstore_sales.csv", encoding="latin-1")

df["Order Date"] = pd.to_datetime(df["Order Date"])

# Sidebar Filters
region = st.sidebar.selectbox("Select Region", df["Region"].unique())

filtered_df = df[df["Region"] == region]

st.subheader("Filtered Data")
st.write(filtered_df.head())

# Sales by Category
st.subheader("Sales by Category")

category_sales = filtered_df.groupby("Category")["Sales"].sum()

fig, ax = plt.subplots()
category_sales.plot(kind="bar", ax=ax)

st.pyplot(fig)

# Discount vs Profit
st.subheader("Discount vs Profit")

fig2, ax2 = plt.subplots()

sns.scatterplot(data=filtered_df, x="Discount", y="Profit", ax=ax2)

st.pyplot(fig2)