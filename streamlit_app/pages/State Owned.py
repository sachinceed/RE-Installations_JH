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


dfall = pd.read_csv(r'streamlit_app/data/All_Total.csv')
dfST=pd.read_csv(r'streamlit_app/data/SSL compiled report.csv')

with open(r'streamlit_app/data/jhnew.geojson') as f:
    geojson_data = json.load(f)

polygon_shapefile = r'streamlit_app/data/jhnew.geojson'
# Reading and converting to WGS84 CRS
polygon_data = gpd.read_file(polygon_shapefile).to_crs(epsg=4326)
st.sidebar.image("streamlit_app/data/ceed logo.png")




st.header('RENEWABLE ENERGY INSTALLATIONS IN JHARKHAND')

# Streamlit app
#st.title('Jharkhand Map')
st.subheader('Hover Over The Districts for More Information for RE Status in Jharkhand')
st.header('ROOFTOP SOLAR')
# Function to customize tooltip
color_scale = linear.Greens_09.scale(dfall['Grid_Connected_Rooftop_Solar_Capacity_Installed_(in_KWp)'].min(), dfall['Grid_Connected_Rooftop_Solar_Capacity_Installed_(in_KWp)'].max())
def style_function(feature):
    return {
        'fillColor':color_scale(feature['properties']['State_Solar_Capacity']),
        'color': 'white',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.9,
    }
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='CartoDB Positron',min_zoom =7,max_zoom=7)

folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','State_Solar_Capacity','State_Solar_Counts',], aliases=['District:','Grid Connected Rooftop Solar capacity(kWp):','Grid Connected Rooftop Solar count:'])

).add_to(m)
# Add color scale legend with white fonts
color_scale.caption = 'Installed Capacity (kwp)'
color_scale.add_to(m)

folium.LayerControl().add_to(m)
folium_static(m,width=600,height=400)

dfSRFY=pd.read_csv(r"streamlit_app/data/FY_GSR_insatllations.csv")
#Grid Connected Solar Rooftop Financial year wise counts in Jharkhand
dfSRFY_sorted = dfSRFY.sort_values(by='2022-23', ascending=True)
fig1 = px.bar(dfSRFY_sorted, y='Districts', x=['2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23'],
             title='Grid interactive Solar Rooftop Installation Nos. in Jharkhand',
             labels={'value': 'Installation Counts','variable': 'Financial Years'},
             template='plotly_dark',
             width=600, height=500)
fig1.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig1.update_yaxes(tickmode='array', tickvals=dfSRFY_sorted['Districts'], ticktext=dfSRFY_sorted['Districts'])
#fig1.show()
st.plotly_chart(fig1) 



dfGSRCAP=pd.read_csv(r"streamlit_app/data/FY_GSR_Capacity.csv")
#Grid Connected Solar Rooftop Capacity in Jharkhand
dfGSRCAP_sorted = dfGSRCAP.sort_values(by='2022-23', ascending=True)
fig2 = px.bar(dfSRFY_sorted, y='Districts', x=['2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23'],
             title='Grid interactive Solar Rooftop Capacity(kWp) in Jharkhand',
             labels={'value': 'Installed Capacity(kWp)','variable': 'Financial Years'},
             template='plotly_dark',
             width=600, height=500)
fig2.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig2.update_yaxes(tickmode='array', tickvals=dfSRFY_sorted['Districts'], ticktext=dfSRFY_sorted['Districts'])

#fig2.show()
st.plotly_chart(fig2) 




# Mini_Grid _solar_Count and Capacity Plots
st.header('MINI-GRID SOLAR')
# Read the CSV data

df4mgs=pd.read_csv(r"streamlit_app/data/Solar_Minigrid.csv")
# Function to customize tooltip
color_scale = linear.Greens_09.scale(dfall['Capacity_Solar_Mini_Grid_Plant'].min(), dfall['Capacity_Solar_Mini_Grid_Plant'].max())
def style_function(feature):
    return {
        'fillColor':color_scale(feature['properties']['State_solarMinigrid_Plant_capacity']),
        'color': 'white',
        'weight':2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='CartoDB Positron',min_zoom =7,max_zoom=7)
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','State_SolarGrid_mini_plant','State_solarMinigrid_Plant_capacity'], aliases=['District:','Solar Minigrids count:','Solar Minigrids capacity(kWp):'])
).add_to(m)
folium.LayerControl().add_to(m)
folium_static(m,width=600,height=400)


df_sorted1 =df4mgs.sort_values(by='Minigrid_Capacity(kWp)',ascending=True)
fig3 = px.bar(df_sorted1, 
              y='Districts', 
              x='Minigrid_Capacity(kWp)', 
              text='Minigrid_Capacity(kWp)',  # Add this line for values in bar labels
              barmode='group', 
              title='Minigrid Capacity(kWp)',
              labels={'Minigrid_Capacity(kWp)': 'Capacity (kWp)'},
              template='plotly_dark',
              width=600, height=500)

fig3.update_xaxes(title_text='Capacity (kWp)')
fig3.update_traces(texttemplate='%{text:.2s}(kWp)', textposition='inside')  # Adjust text formatting and position
fig3.update_yaxes(showticklabels=True, showgrid=True, zeroline=True)
st.plotly_chart(fig3)


st.header('SOLAR STREET LIGHTS ')
color_scale = linear.Greens_09.scale(dfall['Solar_Streetlights'].min(), dfall['Solar_Streetlights'].max())
def style_function(feature):
    return {
        'fillColor':color_scale(feature['properties']['Solar_streetlights_Count']),
        'color': 'white',
        'weight':2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='CartoDB Positron',min_zoom =7,max_zoom=71)
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','Solar_streetlights_Count'], aliases=['District:','Solar Street lights Count:'])
).add_to(m)
folium.LayerControl().add_to(m)
folium_static(m,width=600,height=400)

#'Solar Streetlights Installation (Nos.) in Jharkhand
dfSSL=pd.read_csv(r"streamlit_app/data/SSL compiled FY_cap.csv")
#Grid Connected Solar Rooftop Financial year wise counts in Jharkhand
dfSSL_sorted = dfSSL.sort_values(by='FY-20-21', ascending=True)
fig1 = px.bar(dfSSL_sorted, y='District', x=['FY-14-15','FY-15-16','FY-16-17','FY-18-19','FY-19-20','FY-20-21'],
             title='Solar Streetlights Installation (Nos.) in Jharkhand',
             labels={'value': 'Installation Counts','variable': 'Financial Years'},
             template='plotly_dark',
             width=700, height=500)
fig1.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig1.update_yaxes(tickmode='array', tickvals=dfSSL_sorted['District'], ticktext=dfSSL_sorted['District'])
#fig1.show()
st.plotly_chart(fig1) 


st.title('Solar Rooftop Locations in the State of Jharkhand')
st.subheader('Goverment Hospitals')
# Load GeoJSON file
geojson_file = r"streamlit_app/data/Hospitals.geojson"
gdf = gpd.read_file(geojson_file)

# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7,min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=True)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }
# Define a custom icon with color (e.g., red)
#icon = folium.CustomIcon(icon_image=r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\icon.png", icon_size=(30, 30), icon_anchor=(15, 15), popup_anchor=(0, -15))
#icon = folium.Icon(color='red')
# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = f"Location: {row['Location']}\nCapacity: {row['Capacity(In kWp)']} kWp"
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'yellow',icon='star',prefix='fa',icon_color='white')
    ).add_to(m)

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)
folium.LayerControl().add_to(m)

# Display the Folium map using folium_static
folium_static(m, width=700, height=500)



st.subheader('Educational Institutions')

# Load GeoJSON file
geojson_file = r"streamlit_app/data/Educational_Instutions.geojson"
gdf = gpd.read_file(geojson_file)
# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=False)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }

# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = f"Location: {row['Location']}\nCapacity: {row['Capacity(In kWp)']} kWp"
    
    # Customize the icon size (adjust the icon_size parameter)
    icon_size = (2,2)  # Change the size according to your preference
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'black',icon='star',prefix='fa',icon_color='white')
    ).add_to(m)

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)
folium.LayerControl().add_to(m)
# Display the Folium map using folium_static
folium_static(m, width=700, height=500)



st.subheader('District Courts Buildings')

geojson_file =(r"streamlit_app/data/courts.geojson")

gdf = gpd.read_file(geojson_file)

# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=True)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)

# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = f"Location: {row['Location']}\nCapacity: {row['Capacity(In kWp)']} kWp"
    
    # Customize the icon size (adjust the icon_size parameter)
    #icon=r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\police logo.png"
    icon_size = ()  # Change the size according to your preference
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'gray',icon='star',prefix='fa',icon_color='white'),
    ).add_to(m)
folium.LayerControl().add_to(m)
# Display the Folium map using folium_static
folium_static(m, width=700, height=500)






st.subheader('Police Station installed solar panels')

geojson_file =r"streamlit_app/data/Police stations.geojson"
gdf = gpd.read_file(geojson_file)

# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=True)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)

# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = f"Location: {row['Location']}\nCapacity: {row['Capacity(In kWp)']} kWp"
    
    # Customize the icon size (adjust the icon_size parameter)
    #icon=r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\police logo.png"
    icon_size = ()  # Change the size according to your preference
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'blue',icon='star',prefix='fa',icon_color='white'),
    ).add_to(m)
folium.LayerControl().add_to(m)
# Display the Folium map using folium_static
folium_static(m, width=700, height=500)

st.subheader('Other Goverment Buildings')
geojson_file =r"streamlit_app/data/Govt_buildings.geojson"
gdf = gpd.read_file(geojson_file)

# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=True)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)

# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = f"Location: {row['Location']}\nCapacity: {row['Capacity(In kWp)']} kWp"
    
    # Customize the icon size (adjust the icon_size parameter)
    #icon=r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\police logo.png"
    icon_size = ()  # Change the size according to your preference
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'gray',icon='star',prefix='fa',icon_color='white'),
    ).add_to(m)
folium.LayerControl().add_to(m)
# Display the Folium map using folium_static
folium_static(m, width=700, height=500)


#st.header('Utlity grade (Ground Mounted) = PROJECT ONGOING')
st.header('Utility grade (Floating Solar) - PROJECT ONGOING' )
st.header('Utility grade (Canal Top Solar) - WORK IN PROGRESS')












