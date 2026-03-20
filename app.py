import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Airbnb Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("airbnb.csv")

    if "price" in df.columns:
        df["price"] = (
            df["price"].astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
        )
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    for col in ["accommodates", "number_of_reviews", "reviews_per_month", "minimum_nights"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

st.title("Elena de Mena")
st.subheader("Airbnb Dashboard")

st.sidebar.header("Filters")

room_options = sorted(df["room_type"].dropna().unique()) if "room_type" in df.columns else []
selected_rooms = st.sidebar.multiselect("Room type", room_options, default=room_options)

if "neighbourhood" in df.columns:
    neighborhood_col = "neighbourhood"
elif "neighbourhood_group" in df.columns:
    neighborhood_col = "neighbourhood_group"
else:
    neighborhood_col = None

if neighborhood_col:
    neighborhood_options = sorted(df[neighborhood_col].dropna().unique())
    selected_neighborhoods = st.sidebar.multiselect(
        "Neighborhood",
        neighborhood_options,
        default=neighborhood_options
    )
else:
    selected_neighborhoods = []

if "price" in df.columns:
    min_price = float(df["price"].dropna().min())
    max_price = float(df["price"].dropna().max())
    selected_price = st.sidebar.slider(
        "Price range",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )
else:
    selected_price = None

filtered_df = df.copy()

if "room_type" in filtered_df.columns and selected_rooms:
    filtered_df = filtered_df[filtered_df["room_type"].isin(selected_rooms)]

if neighborhood_col and selected_neighborhoods:
    filtered_df = filtered_df[filtered_df[neighborhood_col].isin(selected_neighborhoods)]

if selected_price and "price" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["price"].between(selected_price[0], selected_price[1])
    ]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Listings", len(filtered_df))

with col2:
    avg_price = filtered_df["price"].mean() if "price" in filtered_df.columns else None
    st.metric("Average price", f"${avg_price:,.2f}" if pd.notna(avg_price) else "N/A")

with col3:
    avg_reviews = (
        filtered_df["number_of_reviews"].mean()
        if "number_of_reviews" in filtered_df.columns else None
    )
    st.metric("Average reviews", f"{avg_reviews:.1f}" if pd.notna(avg_reviews) else "N/A")

tab1, tab2 = st.tabs(["Main Analysis", "Extra Analysis"])

with tab1:
    st.subheader("Listing type vs Number of people")

    if "room_type" in filtered_df.columns and "accommodates" in filtered_df.columns:
        chart_data = filtered_df.groupby("room_type")["accommodates"].mean().sort_values()

        fig, ax = plt.subplots()
        chart_data.plot(kind="bar", ax=ax)
        ax.set_xlabel("Room type")
        ax.set_ylabel("Average accommodates")
        ax.set_title("Average number of people by listing type")
        st.pyplot(fig)

    st.subheader("Price by room type")
    if "room_type" in filtered_df.columns and "price" in filtered_df.columns:
        price_data = filtered_df.groupby("room_type")["price"].mean().sort_values()

        fig, ax = plt.subplots()
        price_data.plot(kind="bar", ax=ax)
        ax.set_xlabel("Room type")
        ax.set_ylabel("Average price")
        ax.set_title("Average price by room type")
        st.pyplot(fig)

with tab2:
    st.subheader("Reviews vs Price")
    if "number_of_reviews" in filtered_df.columns and "price" in filtered_df.columns:
        fig, ax = plt.subplots()
        ax.scatter(filtered_df["number_of_reviews"], filtered_df["price"])
        ax.set_xlabel("Number of reviews")
        ax.set_ylabel("Price")
        ax.set_title("Number of reviews vs Price")
        st.pyplot(fig)

    st.subheader("Top neighborhoods by reviews per month")
    if neighborhood_col and "reviews_per_month" in filtered_df.columns:
        top_neighborhoods = (
            filtered_df.groupby(neighborhood_col)["reviews_per_month"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots()
        top_neighborhoods.plot(kind="bar", ax=ax)
        ax.set_xlabel("Neighborhood")
        ax.set_ylabel("Average reviews per month")
        ax.set_title("Top 10 neighborhoods by reviews per month")
        st.pyplot(fig)

st.subheader("Filtered data")
st.dataframe(filtered_df)
