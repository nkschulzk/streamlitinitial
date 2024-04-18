import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    df = pd.read_excel("weather_data.xlsx")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.sidebar.title("Weather Analysis")

df["Station"] = df["Location"].str.split(",", n=1).str[0]

stations = df["Station"].unique()

station1 = st.sidebar.selectbox("Select Station 1", stations)
station2 = st.sidebar.selectbox("Select Station 2", stations)

start_date = st.sidebar.date_input("Select Start Date")
end_date = st.sidebar.date_input("Select End Date")

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = df[(df["Station"].isin([station1, station2])) & (df["Date"] >= start_date) & (df["Date"] <= end_date)]

st.subheader("Weather Data for Selected Stations and Date Range")
st.write(filtered_df)

st.subheader("Data Visualization")

# Max Temperature Line Plot
st.subheader("Max Temperature")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=filtered_df[filtered_df["Station"] == station1], x="Date", y="Temp Max", marker="o", color="blue", label=station1)
sns.lineplot(data=filtered_df[filtered_df["Station"] == station2], x="Date", y="Temp Max", marker="o", color="orange", label=station2)
plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.title("Max Temperature")
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# Precipitation Line Plot
st.subheader("Precipitation")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=filtered_df[filtered_df["Station"] == station1], x="Date", y="Precip Total", marker="o", color="blue", label=station1)
sns.lineplot(data=filtered_df[filtered_df["Station"] == station2], x="Date", y="Precip Total", marker="o", color="orange", label=station2)
plt.xlabel("Date")
plt.ylabel("Precipitation (inches)")
plt.title("Precipitation")
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# Temperature Distribution Histogram
st.subheader("Temperature Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
palette = {station1: "blue", station2: "orange"}
sns.histplot(data=filtered_df, x="Temp Max", hue="Station", kde=True, palette=palette)
plt.xlabel("Temperature (°F)")
plt.ylabel("Frequency")
plt.title("Temperature Distribution")
plt.legend(title="Station")
st.pyplot(fig)

# Boxplot of temperatures for the two selected locations
st.subheader("Boxplot of Temperature for Selected Locations")
fig, ax = plt.subplots(figsize=(10, 6))
station1_data = filtered_df[filtered_df["Station"] == station1]["Temp Max"]
station2_data = filtered_df[filtered_df["Station"] == station2]["Temp Max"]
sns.boxplot(data=[station1_data, station2_data], ax=ax)
ax.set_xticklabels([station1, station2])
plt.xlabel("Stations")
plt.ylabel("Max Temperature (°F)")
st.pyplot(fig)