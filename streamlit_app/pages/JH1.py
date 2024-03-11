import streamlit as st
import pandas as pd
import folium
import json

# Function to load data
@st.cache
def load_data():
    dfall = pd.read_csv('streamlit_app/data/All_Total_.csv')
    with open('streamlit_app/data/jhnew.geojson') as f:
        geojson_data = json.load(f)
    return dfall, geojson_data

# Function to calculate metrics
@st.cache
def calculate_metrics(filtered_df):
    sum_households = int(filtered_df['Count_Solar_Mini_Grid_Plant'].sum())
    sum_minigrid_capacity = int(filtered_df['Capacity_Solar_Mini_Grid_Plant'].sum())
    sum_sgmp_capacity = int(filtered_df['SGM_Capacity'].sum())
    sum_rooftop_capacity = int(filtered_df['Grid_Connected_Rooftop_Solar_Capacity_Installed_(in_KWp)'].sum())
    sum_rooftop_installations = int(filtered_df['Total_Number_of_Building_solar_rooftop_grid_connected'].sum())
    sum_solar_pumps = int(filtered_df['Count_solar_pump_installed'].sum())
    sum_private_rooftop_installations = int(filtered_df['private_solar_total_count'].sum())
    sum_utility_Grade_Solar = int(filtered_df['SGM_Capacity'].sum())
    sum_privatesolar_capacity = int(filtered_df['Privatesolartotalcapacity'].sum())
    sum_ongrid_capacity = int(filtered_df[['Grid_Connected_Rooftop_Solar_Capacity_Installed_(in_KWp)','Privatesolartotalcapacity']].sum().sum())
    sum_offgrid_capacity = int(filtered_df[['Capacity_Solar_Mini_Grid_Plant','SGM_Capacity','Solar_Streetlights_capacity']].sum().sum())
    sum_solar_street_lights = int(filtered_df['Solar_street_Lights'].sum())
    sum_solar_SL_capacity = int(filtered_df['Solar_Streetlights_capacity'].sum())
    sum_Hydro_power = int(filtered_df['Hydro_Power'].sum())
    sum_Bio_power = int(filtered_df['Bio_Power'].sum())
    return (sum_households, sum_minigrid_capacity, sum_sgmp_capacity, sum_rooftop_capacity, sum_rooftop_installations, 
            sum_solar_pumps, sum_private_rooftop_installations, sum_utility_Grade_Solar, sum_privatesolar_capacity, 
            sum_ongrid_capacity, sum_offgrid_capacity, sum_solar_street_lights, sum_solar_SL_capacity, sum_Hydro_power, 
            sum_Bio_power)

# Load data
dfall, geojson_data = load_data()

# Sidebar district selection
districts = ['Jharkhand'] + dfall['District'].unique().tolist()
selected_district = st.sidebar.selectbox('Select a District to get all details of Installations', districts)

# Filter data based on selected district
if selected_district == 'Jharkhand':
    filtered_dfall = dfall  # Return the entire DataFrame for Jharkhand
else:
    filtered_dfall = dfall[dfall['District'] == selected_district]

# Calculate metrics
(sum_households, sum_minigrid_capacity, sum_sgmp_capacity, sum_rooftop_capacity, sum_rooftop_installations, 
 sum_solar_pumps, sum_private_rooftop_installations, sum_utility_Grade_Solar, sum_privatesolar_capacity, 
 sum_ongrid_capacity, sum_offgrid_capacity, sum_solar_street_lights, sum_solar_SL_capacity, sum_Hydro_power, 
 sum_Bio_power) = calculate_metrics(filtered_dfall)

# Display main title
st.title('Renewable Energy Dashboard For The State of Jharkhand')

# Display GeoJSON map
st.subheader('Hover over The Districts To Get More Information Of RE Status In The State Of Jharkhand')
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7,min_zoom=5, max_zoom=15, tiles='cartodb dark_matter', control_scale=True)

# Customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }

# Add GeoJSON layer to the map
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','State_Solar_Counts','State_Solar_Capacity','State_Solarpump_counts','State_solarMinigrid_Plant_capacity','State_SolarGrid_mini_plant','SGM_count','SGM_Capacity','Solar_streetlights','pvt_SOLAR_TCOUNTS'], 
                                 aliases=['District:','Grid Connected Solar Rooftop(Nos.)','Grid Connected Solar Rooftop Capacity(kWp)','Solar Pump (Nos.)','Minigrid Solar Capacity(kWp)','Minigrid Solar(Nos.)','Solar Ground Mounted(Nos.)','Solar Ground Mounted Capacity(Kwp)','Solar street lights(Nos.)','Private Solar(Nos.)'])
).add_to(m)

# Lock the zoom level
m.options['scrollWheelZoom'] = False

# Display map
st.write(m, width=1400, height=500)

# Display selected district
st.header(selected_district)

# Define metrics columns
col1, col2, col3 = st.columns(3)

# Display metrics in columns
with col1:
    st.header('Total On-Grid Capacity')
    st.metric(label=" ", value=f"{sum_ongrid_capacity} kWp")
    st.header('Total Off-Grid Capacity')
    st.metric(label=" ", value=f"{sum_offgrid_capacity} kWp")
with col2:
    st.header('State Owned')
    st.metric(label="Rooftop Solar Capacity (kWp)", value=f"{sum_rooftop_capacity} kWp")
    st.metric(label="Rooftop Solar Nos.", value=sum_rooftop_installations)
    st.metric(label="Minigrid capacity (kWp)", value=f"{sum_minigrid_capacity} kWp")
    st.metric(label="Minigrid Solar (Nos.)", value=sum_households)
    st.metric(label="Bio Power Capacity", value=f"{sum_Bio_power}MW")
    st.metric(label="Hydro Power Capacity ", value=f"{sum_Hydro_power}MW")

# Display Private Owned metrics
with col3:
    st.header('Private Owned')
    st.metric(label="Rooftop Solar Capacity(kWp)", value=f"{sum_privatesolar_capacity} kWp")
    st.metric(label="Rooftop Solar Nos.", value=sum_private_rooftop_installations)
    st.metric(label="Utility-Grade capacity(kWp)", value=f"{sum_utility_Grade_Solar} kWp")
    st.metric(label="Solar Water Pumps Nos.", value=sum_solar_pumps)
