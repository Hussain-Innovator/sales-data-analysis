import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ───────────────────────────────────────────────────────────────
# Title & basic setup
# ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")
st.title("Superstore Sales Dashboard")


# ───────────────────────────────────────────────────────────────
# Load data with robust path + caching + error handling
# ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "data", "superstore_sales.csv")
    
    try:
        df = pd.read_csv(csv_path, encoding="latin-1")
        st.success("Data loaded successfully! (Rows: " + str(len(df)) + ")")
        return df
    except FileNotFoundError:
        st.error(f"❌ File not found: {csv_path}")
        st.error("Make sure:")
        st.error("1. 'data' folder exists in GitHub repo root")
        st.error("2. File is named exactly 'superstore_sales.csv' (case-sensitive)")
        st.error("3. File was committed & pushed to GitHub")
        st.stop()
    except Exception as e:
        st.error("Other error while loading CSV:")
        st.error(str(e))
        st.stop()

# Load the data
df = load_data()

# Convert date column
df["Order Date"] = pd.to_datetime(df["Order Date"])

# ───────────────────────────────────────────────────────────────
# Sidebar Filters
# ───────────────────────────────────────────────────────────────
st.sidebar.header("Filters")

# Region filter
region = st.sidebar.selectbox("Select Region", ["All"] + list(df["Region"].unique()))

# Apply filter
if region == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Region"] == region]

st.subheader(f"Filtered Data ({len(filtered_df)} rows)")
st.dataframe(filtered_df.head(10))  # showing more rows for better preview

# ───────────────────────────────────────────────────────────────
# Sales by Category
# ───────────────────────────────────────────────────────────────
st.subheader("Sales by Category")

category_sales = filtered_df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
category_sales.plot(kind="bar", ax=ax, color="skyblue")
ax.set_ylabel("Total Sales")
ax.set_title(f"Sales by Category - {region}")
plt.tight_layout()

st.pyplot(fig)

# ───────────────────────────────────────────────────────────────
# Discount vs Profit Scatter
# ───────────────────────────────────────────────────────────────
st.subheader("Discount vs Profit")

fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.scatterplot(
    data=filtered_df,
    x="Discount",
    y="Profit",
    hue="Category",
    size="Sales",
    sizes=(20, 200),
    alpha=0.7,
    ax=ax2
)
ax2.set_title(f"Discount vs Profit - {region}")
plt.tight_layout()

st.pyplot(fig2)

# Optional: small note at the bottom
st.markdown("---")
st.caption("Dashboard built with Streamlit • Data: Superstore Sales")