import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import folium
import plotly.express as px
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import json
from branca.colormap import linear
from streamlit_folium import folium_static

st.subheader('ROOFTOP SOLAR INSTALLED BY DVC')

with open(r'streamlit_app/data/jhnew.geojson') as f:
    geojson_data = json.load(f)

dfall = pd.read_csv(r'streamlit_app/data/All_Total.csv')


# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'white',
        'weight':2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='cartodb dark_matter',min_zoom =7,max_zoom=7,zoomControl=False)
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','DVC_solar'], aliases=['District:','INSTALLED CAPACITY (kwp) BY DVC'])
).add_to(m)
folium.LayerControl().add_to(m)
folium_static(m,width=600,height=400)


st.subheader('colour Gradient Map')


# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': color_scale(feature['properties']['DVC_solar']),
        'color': 'white',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }

# Create a color scale
color_scale = linear.PuBu_09.scale.scale(dfall['DVC_owned_Solar(kwp)'].min(), dfall['DVC_owned_Solar(kwp)'].max())

# Create the map
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='cartodb dark_matter', min_zoom=7, max_zoom=7,zoomControl=False)

# Add GeoJson layer with customized style and tooltip
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname', 'DVC_solar'], aliases=['District:', 'INSTALLED CAPACITY (kwp) BY DVC'])
).add_to(m)

# Add color scale legend
color_scale.caption = 'Installed Capacity (kwp)'
color_scale.add_to(m)

# Add LayerControl
folium.LayerControl().add_to(m)

# Display the map
folium_static(m, width=800, height=600)






