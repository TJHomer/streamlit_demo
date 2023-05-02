import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import leafmap.foliumap as leafmap



st.set_page_config(layout="wide")

def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


st.title("Select a Basemap")


col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    
    selection = st.radio("Use a preloaded basemap or enter a url", 
                         ("Preloaded", "URL"))
    

    if selection == "Preloaded":
        basemap = st.selectbox("Select a basemap:", options, index)
    
    if selection == "URL":
        url = st.text_input(
        "Enter a WMS URL:", value="https://services.terrascope.be/wms/v2"
        )
        empty = st.empty()
        default = None

        if url:
            options = get_layers(url)
    
            layers = empty.multiselect(
                "Select WMS layers to add to the map:", options, default=default)
    

    st.markdown("""
    Go to https://apps.nationalmap.gov/services to find some WMS URLs if needed.
    """)

with col1:
    if selection == "Preloaded":
        m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
        m.add_basemap(basemap)
    
    if selection == "URL":
        m = leafmap.Map(center=(36.3, 0), zoom=2)
        if layers is not None:
            for layer in layers:
                m.add_wms_layer(
                    url, layers=layer, name=layer, attribution=" ", transparent=True
                )


    m.to_streamlit(height=700)

