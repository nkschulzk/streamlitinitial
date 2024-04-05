import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the popular names dataset
url = 'https://github.com/esnt/Data/raw/main/Names/popular_names.csv'
data= pd.read_csv(url)


# Title of the app
st.title("Popular Baby Names App")

# Sidebar for user input
st.sidebar.title("Filters")
gender = st.sidebar.radio("Select Gender", ("Both", "M", "F"))
year_range = st.sidebar.slider("Select Year Range", min_value=data['year'].min(), max_value=data['year'].max(), value=(data['year'].min(), data['year'].max()))

# Filter data based on user input
filtered_data = data[(data['year'] >= year_range[0]) & (data['year'] <= year_range[1])]
if gender != "Both":
    filtered_data = filtered_data[filtered_data['sex'] == gender]

# Show data based on user input
st.write("### Displaying Names Data")
st.write(filtered_data)

# Expander for additional information
with st.expander("Additional Information"):
    st.write("This dataset contains popular baby names from 1880 to 2008.")

# Popover with instructions
st.write("Hover over the interactive elements for instructions")
st.markdown(
    """
    <details>
    <summary>Instructions</summary>
    <p>To interact with the sidebar, select the gender and year range to filter the data.</p>
    </details>
    """,
    unsafe_allow_html=True
)

# Generate a graph based on the filtered data
st.write("### Interactive Graph")
selected_names = st.multiselect("Select Names", filtered_data['name'].unique())
if selected_names:
    selected_data = filtered_data[filtered_data['name'].isin(selected_names)]
    plt.figure(figsize=(10, 6))
    for name in selected_names:
        name_data = selected_data[selected_data['name'] == name]
        plt.plot(name_data['year'], name_data['n'], label=name)
    plt.xlabel("Year")
    plt.ylabel("Number of Babies")
    plt.legend()
    st.pyplot()

# Tabs for different sections
with st.sidebar:
    st.title("About")
    st.write("This app displays popular baby names data.")