import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    df = pd.read_excel("weather_data.xlsx")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.write("""
# Weather Analysis

This app allows you to analyze weather data from different stations over a specified date range.
You can select two stations, choose a date range, and visualize various weather metrics. Utilize the sidebar to do so.
         
The main questions I wanted to address were how time effects the precipitation and temperature and how locations distributions and temperatures compare.

To allow you more control in this exploration, I left the options to compare different locations as well as select the type of data you want to compare for each.
""")

st.sidebar.title("Weather Analysis")

df["Station"] = df["Location"].str.split(",", n=1).str[0]

selected_stations = st.sidebar.multiselect("Select Stations", df["Station"].unique())

start_date = st.sidebar.date_input("Select Start Date")
end_date = st.sidebar.date_input("Select End Date")

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

temperature_metric = st.sidebar.selectbox("Select Temperature Metric", ["Temp Max", "Temp Avg", "Temp Min"])

filtered_df = df[(df["Station"].isin(selected_stations)) & (df["Date"] >= start_date) & (df["Date"] <= end_date)]

st.subheader("Weather Data for Selected Stations and Date Range")
st.write(filtered_df)

st.subheader("Data Visualization")

# Max Temperature Line Plot
st.subheader(temperature_metric)
fig, ax = plt.subplots(figsize=(10, 6))
for station in selected_stations:
    sns.lineplot(data=filtered_df[filtered_df["Station"] == station], x="Date", y=temperature_metric, marker="o", label=station)
plt.xlabel("Date")
plt.ylabel(f"{temperature_metric} (°F)")
plt.title(temperature_metric)
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# Precipitation Line Plot
st.subheader("Precipitation")
fig, ax = plt.subplots(figsize=(10, 6))
for station in selected_stations:
    sns.lineplot(data=filtered_df[filtered_df["Station"] == station], x="Date", y="Precip Total", marker="o", label=station)
plt.xlabel("Date")
plt.ylabel("Precipitation (inches)")
plt.title("Precipitation")
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# Temperature Distribution Histogram
st.subheader("Temperature Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
palette = sns.color_palette("husl", len(selected_stations))
for i, station in enumerate(selected_stations):
    sns.histplot(data=filtered_df[filtered_df["Station"] == station], x=temperature_metric, kde=True, color=palette[i], label=station)
plt.xlabel(f"{temperature_metric} (°F)")
plt.ylabel("Frequency")
plt.title("Temperature Distribution")
plt.legend(title="Station")
st.pyplot(fig)

# Boxplot of temperatures for the selected locations
st.subheader("Boxplot of Temperature for Selected Locations")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_df, x="Station", y=temperature_metric, ax=ax)
plt.xlabel("Station")
plt.ylabel(f"{temperature_metric} (°F)")
plt.xticks(rotation=45)
st.pyplot(fig)