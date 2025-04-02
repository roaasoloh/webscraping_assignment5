# dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="eBay Deals Dashboard", layout="wide")

# Load the dataset
@st.cache_data #Streamlit caching decorator used to optimize performance by preventing repeated reloading or recomputation of data
def load_data():
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    return df

df = load_data()

# Sidebar filters
st.sidebar.header(" Filter Deals")

# Hour filter
hour_range = st.sidebar.slider("Filter by Hour", 0, 23, (0, 23))
filtered_df = df[df['hour'].between(hour_range[0], hour_range[1])]

# Price range filter
min_price = float(filtered_df['price'].min())
max_price = float(filtered_df['price'].max())
price_range = st.sidebar.slider("Filter by Price ($)", min_price, max_price, (min_price, max_price))
filtered_df = filtered_df[filtered_df['price'].between(price_range[0], price_range[1])]

# Keyword filter
st.sidebar.markdown("**Search by Keyword in Title**")
keyword = st.sidebar.text_input("Keyword (e.g., Apple, Laptop)", "").strip().lower()
if keyword:
    filtered_df = filtered_df[filtered_df['title'].str.lower().str.contains(keyword)]

# --- Dashboard Layout ---
st.title("🛍️ eBay Tech Deals Dashboard")
st.markdown(f"Showing **{len(filtered_df)}** deals between **{hour_range[0]}:00 and {hour_range[1]}:00** priced between **${price_range[0]} and ${price_range[1]}**")

# Column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Deals Per Hour")
    deals_per_hour = filtered_df.groupby("hour").size()
    fig1, ax1 = plt.subplots()
    deals_per_hour.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Number of Deals")
    ax1.set_title("Deals Per Hour")
    st.pyplot(fig1)

with col2:
    st.subheader("💸 Price Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(filtered_df["price"], bins=10, kde=True, ax=ax2, color='lightgreen')
    ax2.set_title("Product Price Distribution")
    st.pyplot(fig2)

# Scatter Plot: Original vs Discounted
st.subheader(" Original vs Discounted Price")
fig3, ax3 = plt.subplots()
sns.scatterplot(data=filtered_df, x="original_price", y="price", ax=ax3)
ax3.set_xlabel("Original Price")
ax3.set_ylabel("Discounted Price")
st.pyplot(fig3)

# Top 5 Best Deals
st.subheader("🏆 Top 5 Best Deals (Highest Discounts)")
top_deals = filtered_df.sort_values(by="discount_percentage", ascending=False).head(5)
st.table(top_deals[["title", "price", "original_price", "discount_percentage", "shipping"]])
