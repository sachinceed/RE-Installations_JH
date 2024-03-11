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


# Set the page configuration to wide mode
st.set_page_config(layout="wide")

st.subheader('ROOFTOP SOLAR INSTALLED BY DVC')
#st.sidebar.image("streamlit_app/data/ceed logo.png")

with open(r'streamlit_app/data/jhnew.geojson') as f:
    geojson_data = json.load(f)

dfall = pd.read_csv(r'streamlit_app/data/All_Total_.csv')
# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': color_scale(feature['properties']['DVC_solar']),
        'color': 'black',
        'weight': 0.7,
        'dashArray': '4, 4',
        'fillOpacity': 3.0,
    }

# Create a color scale
color_scale = linear.Greens_09.scale(dfall['DVC_owned_Solar(kwp)'].min(), dfall['DVC_owned_Solar(kwp)'].max())

# Create the map
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='CartoDB Positron', min_zoom=7, max_zoom=7,zoomControl=True)

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
# Lock the zoom level
m.options['scrollWheelZoom'] = False
# Display the map
#folium_static(m, width=600, height=400)



dfall = pd.read_csv(r'streamlit_app/data/All_Total_.csv')
dfDVC_sorted = dfall.sort_values(by='DVC_owned_Solar(kwp)', ascending=True)
fig3 = px.bar(dfDVC_sorted, y='District', x='DVC_owned_Solar(kwp)',
             title='DVC Solar Installations in Jharkhand',
             labels={'value': 'Installation Capacity(kWp)','variable': 'Financial Years'},
              text='DVC_owned_Solar(kwp)',
             template='plotly_dark',
             width=600, height=500)
fig3.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig3.update_yaxes(tickmode='array', tickvals=dfDVC_sorted['District'], ticktext=dfDVC_sorted['District'])
fig3.update_yaxes(showticklabels=True, showgrid=True, zeroline=True)
#fig1.show()

row1, row2 = st.columns(2)
with row1:
    folium_static(m,width=600,height=500)
with row2:
    st.plotly_chart(fig3)






