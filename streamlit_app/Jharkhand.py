import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import json
import branca.colormap as cm
from streamlit_folium import folium_static


# Set Streamlit page title and header
st.set_page_config(page_title='Decentralized Renewable Energy',layout="wide")


# Assuming imagePath is the path to your image file and link is the URL you want to redirect to
imagePath = 'streamlit_app/data/ceed logo.png'
link = "https://ceedindia.org/"

# Use st.sidebar.markdown to embed an HTML link with the image
st.sidebar.image(f'<a href="{link}" target="_blank"><img src="{imagePath}" width="100" alt="Sidebar Image"></a>', unsafe_allow_html=True)
#st.sidebar.image("streamlit_app/data/ceed logo.png")






st.title('Renewable Energy (RE) Dashboard For The State of Jharkhand')

# Read the CSV data
dfall = pd.read_csv('streamlit_app/data/All_Total.csv')

# Load GeoJSON data
with open('streamlit_app/data/jhnew.geojson') as f:
    geojson_data = json.load(f)

st.subheader('Hover over The Districts To Get More Information Of RE Status In The State Of Jharkhand')

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }

# Function to filter data based on selected district
def filter_data_by_district(district):
    if district == 'Jharkhand':
        return dfall  # Return the entire DataFrame for Jharkhand
    else:
        filtered_dfall = dfall[dfall['District'] == district]
        return filtered_dfall
    
# Sidebar district selection
districts = ['Jharkhand'] + dfall['District'].unique().tolist()  # Add 'Jharkhand' to the list of districts
selected_district = st.sidebar.selectbox('Select a District to get all details of Installations', districts)

# Filter data based on selected district
filtered_dfall = filter_data_by_district(selected_district)
print(filtered_dfall)

m = folium.Map(location=[23.6345, 85.3803], zoom_start=7,min_zoom=5, max_zoom=15, tiles='cartodb dark_matter', control_scale=True)
#folium.TileLayer('cartodbpositron', name='Light Map').add_to(m)  # Add light map layer
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','State_Solar_Counts','State_Solar_Capacity','State_Solarpump_counts','State_solarMinigrid_Plant_capacity','State_SolarGrid_mini_plant','SGM_count','SGM_Capacity','Solar_streetlights','PRIVATE_SOLAR(19-20)','PRIVATE_SOLAR_ROOFTOP'], 
                                 aliases=['District:','Grid Connected installed Solar Rooftop Counts(No.)','Grid Connected Solar Rooftop Capacity(kWp)','Solar Pump Counts(No.)','Minigrid Solar Capacity(kWp)','Minigrid Solar installed Counts(No.)','Solar Ground Mounted Counts(No.)','Solar Ground Mounted Capacity(Kwp)','Solar street lights Count(No.)','Private solarrooftop installed 19-20','Private solarrooftop installed 22-23'])
).add_to(m)

# Lock the zoom level
m.options['scrollWheelZoom'] = False

folium.LayerControl().add_to(m)





# Calculate metrics from filtered data
sum_households = int(filtered_dfall['Count_Solar_Mini_Grid_Plant'].sum())
sum_minigrid_capacity = int(filtered_dfall['Capacity_Solar_Mini_Grid_Plant'].sum())
sum_sgmp_capacity = int(filtered_dfall['SGM_Capacity'].sum())
sum_rooftop_capacity = int(filtered_dfall['Grid_Connected_Rooftop_Solar_Capacity_Installed_(in_KWp)'].sum())
sum_rooftop_installations = int(filtered_dfall['Total_Number_of_Building_solar_rooftop_grid_connected'].sum())
sum_solar_pumps = int(filtered_dfall['Count_solar_pump_installed'].sum())
sum_private_rooftop_installations = int(filtered_dfall['private_solar_total_count'].sum())
sum_utility_Grade_Solar = int(filtered_dfall['SGM_Capacity'].sum())
sum_privatesolar_capacity = int(filtered_dfall['Privatesolartotalcapacity'].sum())
sum_ongrid_capacity = int(filtered_dfall[['Grid_Connected_Rooftop_Solar_Capacity_Installed_(in_KWp)','Privatesolartotalcapacity']].sum().sum())
sum_offgrid_capacity = int(filtered_dfall[['Capacity_Solar_Mini_Grid_Plant','SGM_Capacity','Solar_Streetlights_capacity']].sum().sum())
sum_solar_street_lights = int(filtered_dfall['Solar_street_Lights'].sum())
sum_solar_SL_capacity = int(filtered_dfall['Solar_Streetlights_capacity'].sum())
#total_capacity=filtered_dfall['Capacity_Solar_Mini_Grid_Plant','SGM_Capacity','Grid_Connected_Rooftop_Solar_Capacity_Installed_(in_KWp)']
# Display metrics



row1, row2 = st.columns(2)
with row1:
    folium_static(m, width=600, height=400)
with row2:
    st.header('Total On-Grid Capacity')
    st.metric(label=" ", value=f"{sum_ongrid_capacity} kWp")
    st.header('Total Off-Grid Capacity')
    st.metric(label=" ", value=f"{sum_offgrid_capacity} kWp")


st.header('State Owned')
st.metric(label=' ', value=selected_district)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Rooftop Solar Nos.", value= sum_private_rooftop_installations)
with col2:
    st.metric(label="Minigrid Solar Nos.", value = sum_households)
with col3:
    st.metric(label="Solar Streetlights Nos.", value = sum_solar_street_lights)  
with col4:
    st.metric(label="Solar Water Pumps Nos.", value= sum_solar_pumps)

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(label="Rooftop Solar Capacity ", value=f"{sum_rooftop_capacity} kWp")
with col6:
    st.metric(label="Minigrid capacity", value=f"{sum_minigrid_capacity} kWp")
with col7:
    st.metric(label="Solar Street Lights Capacity", value = f"{sum_solar_SL_capacity} kWp")   



st.header('Private Owned')

col8, col9, col10,col11 = st.columns(4)
with col8:
    st.metric(label="Rooftop Solar Capacity", value=f"{sum_privatesolar_capacity} kWp")
with col9:
    st.metric(label="Rooftop Solar Nos.", value=sum_private_rooftop_installations)
with col10:
    st.metric(label="Utility-Grade capacity", value=f"{sum_utility_Grade_Solar} kWp")
with col11:
    st.metric(label="Solar Water Pumps Nos.", value=sum_solar_pumps)






#st.header('Total Solar Capacity')
#st.metric(label=" ", value= )




