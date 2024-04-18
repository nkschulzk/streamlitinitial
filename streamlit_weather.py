import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    df = pd.read_excel("adj_weather_data.xlsx")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.write("""
# Weather Analysis

This app allows you to analyze weather data from different ski resorts or surrounding areas over a specified date range.
You can select two stations, choose a date range, and visualize various weather metrics. Utilize the sidebar to do so.
         
The main questions I wanted to address were how time effects the precipitation and temperature and how locations distributions and temperatures compare.

To allow you more control in this exploration, I left the options to compare different locations as well as select the type of data you want to compare for each.
""")

st.sidebar.title("Weather Analysis")

selected_resorts = st.sidebar.multiselect("Select Resorts", df["ResortName"].unique())

start_date = st.sidebar.date_input("Select Start Date")
end_date = st.sidebar.date_input("Select End Date")

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

temperature_options = ["Local Temp", "Resort Temp"]
selected_temperature = st.sidebar.radio("Select Temperature Metric", temperature_options)

if selected_temperature == "Local Temp":
    temperature_metric = "Temp Avg"
elif selected_temperature == "Resort Temp":
    temperature_metric = "adj_temp"

filtered_df = df[(df["ResortName"].isin(selected_resorts)) & (df["Date"] >= start_date) & (df["Date"] <= end_date)]

st.subheader("Weather Data for Selected Resorts and Date Range")
st.write(filtered_df)

st.subheader("Data Visualization")

# Max Temperature Line Plot
st.subheader(temperature_metric)
fig, ax = plt.subplots(figsize=(10, 6))
for resort in selected_resorts:
    sns.lineplot(data=filtered_df[filtered_df["ResortName"] == resort], x="Date", y=temperature_metric, marker="o", label=resort)
plt.xlabel("Date")
plt.ylabel(f"{temperature_metric} (°F)")
plt.title(temperature_metric)
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# Precipitation Line Plot
st.subheader("Precipitation")
fig, ax = plt.subplots(figsize=(10, 6))
for resort in selected_resorts:
    sns.lineplot(data=filtered_df[filtered_df["ResortName"] == resort], x="Date", y="Precip Total", marker="o", label=resort)
plt.xlabel("Date")
plt.ylabel("Precipitation (inches)")
plt.title("Precipitation")
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# Temperature Distribution KDE Plot
st.subheader("Temperature Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
palette = sns.color_palette("husl", len(selected_resorts))
for i, resort in enumerate(selected_resorts):
    sns.kdeplot(data=filtered_df[filtered_df["ResortName"] == resort][temperature_metric], color=palette[i], label=resort)
plt.xlabel(f"{temperature_metric} (°F)")
plt.ylabel("Density")
plt.title("Temperature Distribution")
plt.legend(title="Resort")
st.pyplot(fig)

# Boxplot of temperatures for the selected resorts
st.subheader("Boxplot of Temperature for Selected Resorts")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_df, x="ResortName", y=temperature_metric, ax=ax)
plt.xlabel("Resort")
plt.ylabel(f"{temperature_metric} (°F)")
plt.xticks(rotation=45)
st.pyplot(fig)