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

selected_visual = st.sidebar.selectbox("Select Visualization", ["below_32", "snowday", "overlay"])

filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

st.subheader("Weather Data for Selected Resorts and Date Range")
st.write(filtered_df)

st.subheader("Data Visualization")

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

st.subheader("Boxplot of Temperature for Selected Resorts")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_df, x="ResortName", y=temperature_metric, ax=ax)
plt.xlabel("Resort")
plt.ylabel(f"{temperature_metric} (°F)")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Counts of Days Below Freezing or Snow Days for All Resorts")
if selected_visual == "below_32":
    count_data = filtered_df.groupby("ResortName")["below_32"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=count_data, x="ResortName", y="below_32", ax=ax)
    ax.set_xlabel("Resort")
    ax.set_ylabel("Days Below Freezing")
    ax.set_xticklabels(count_data["ResortName"], rotation=45)
    st.pyplot(fig)
elif selected_visual == "snowday":
    count_data = filtered_df.groupby("ResortName")["snowday"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=count_data, x="ResortName", y="snowday", ax=ax)
    ax.set_xlabel("Resort")
    ax.set_ylabel("Snow Days")
    ax.set_xticklabels(count_data["ResortName"], rotation=45)
    st.pyplot(fig)
elif selected_visual == "overlay":
    count_data_below_32 = filtered_df.groupby("ResortName")["below_32"].sum().reset_index()
    count_data_snowday = filtered_df.groupby("ResortName")["snowday"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=count_data_below_32, x="ResortName", y="below_32", color="blue", label="Days Below Freezing", ax=ax)
    sns.barplot(data=count_data_snowday, x="ResortName", y="snowday", color="orange", label="Snow Days", ax=ax)
    ax.set_xlabel("Resort")
    ax.set_ylabel("Count")
    ax.set_xticklabels(count_data_below_32["ResortName"], rotation=45)
    ax.legend()
    st.pyplot(fig)