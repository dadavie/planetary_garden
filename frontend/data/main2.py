import streamlit as st
# from popup_map import plot_map
from address_to_latlon.address_conversion import coordinates_from_address
import plotly.express as px
import numpy as np
import pandas as pd
import requests


from streamlit_folium import folium_static
# st_folium
import folium
import os
import base64
from PIL import Image
import io



st.set_page_config(layout="wide")

Header=st.container()
Climate_Map =st.container()
Garden = st.container()
Moving_Out = st.container()
Moving_In = st.container()


# st.markdown(
#     """
#     <style>
#     .main {
#     background-color: #6b754b ;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

def plot_map(df, lat, lon):
    points=[[lat+0.5, lon+0.5], [lat+1, lon+1], [lat-1, lon-0.92], [lat-0.87, lon+0.97], [lat+1, lon-1], [lat-0.24, lon-0.5],[lat+0.32, lon-0.6],[lat-0.56, lon+0.78],[lat-0.13, lon-0.1],[lat+0.89, lon-0.34], [lat-0.8, lon+0.6], [lat+0.02, lon-0.3], [lat-0.75, lon-0.74], [lat+0.15, lon+0.56], [lat-0.4, lon+0.56], [lat+1, lon+1]]
    map = folium.Map(location=[lat, lon], zoom_start=9, tiles="Stamen Terrain", width=1300, height=700)

    # file_ = open("../static/photos/butterfly.jpg", "rb")
    # contents = file_.read()
    # data_url = base64.b64encode(contents).decode("utf-8")
    # file_.close()
    #file_=open(f"../static/photos/{i[0]}.jpg", "rb")
    #file_=open(f"https://storage.googleapis.com/planetary/{i[0]}.jpg", "rb")


    for i,row in df.iterrows():
        url = f"https://storage.googleapis.com/planetary/{row['thumbnails']}.jpg"
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        img.save("tmp.jpg")
        file_= open("tmp.jpg", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        # file_= Image.open(f"https://storage.googleapis.com/planetary/{i[0]}.jpg")
        # contents = file_.read()
        # data_url = base64.b64encode(contents).decode("utf-8")
        # file_.close()

        html = folium.Html(
                f"""
                <!DOCTYPE html>
                <html>
                <p> {row['species']} </p>

                <center>
                    <img src="data:image/jpg;base64,{data_url}" width="70" style="border-radius: 50px;"/>
                </center>

        </html>

        """, script=True)
        if row['at_risk']==1:
            color='red'
        else:
            color='yellow'

        popup  = folium.Popup(html, max_width=120, max_height= 120, show=True)
        folium.vector_layers.Marker(location=points[i],popup = popup,icon= folium.Icon(color=color, icon_color='black',icon = 'globe')).add_to(map)

    st_data = folium_static(map, width = 1525)

def input_coords():
    input_lat= st.number_input('insert latitude (-90 to 90)')
    input_lon= st.number_input('insert longitude (-180 to 180)')
    return input_lat, input_lon


def fetch( url):
    try:
        result = requests.get(url)
        return result.json()
    except Exception:
        return {}

# session = requests.Session()

with Header:
    st.title ('Welcome to our Planetary Garden')


with Climate_Map:
    st.header('Climate Map')
    st.subheader('Select climate future for your garden:')
    clim_scen_col, free_space_1, year_slider_col, free_space_2 = st.columns([1,0.5,1,1.5], gap="medium")

    scenario_selected = clim_scen_col.selectbox(
        'Climate Scenario',
        options=['1. Sustainability',
                 '2. Middle of the Road',
                 '3. Regional Rivalry',
                 '4. Fossil-Fueled Development'],
        index=0
        )
    scenario_dict = {
        '1. Sustainability':'ssp126',
        '2. Middle of the Road': 'ssp245',
        '3. Regional Rivalry': 'ssp370',
        '4. Fossil-Fueled Development': 'ssp585'
    }
    # scenario_dict = {
    #     'Sustainability (Taking the Green Road)':'ssp126',
    #     'Middle of the Road': 'ssp245',
    #     'Regional Rivalry (A Rocky Road)': 'ssp370',
    #     'Fossil-Fueled Development (Taking the Highway)': 'ssp585'
    # }
    scenario = scenario_dict[scenario_selected]
    year = year_slider_col.select_slider('Year', options=['2040', '2060', '2080', '2100'], value='2100')
    # no_clusters = slider_col.select_slider('Number of clusters', options=['20', '30', '60', '100'], value='60')



# # Plotly stuff
# rr = np.load('plotly_data/frontend_info_future_maps.npy', allow_pickle=True)
# ## input from streamlit slider
# #scenario = slider_col.selectbox('Climate Scenario', options=['SSP126', 'SSP245', 'SSP370', 'SSP585'], index=2)
# #year = slider_col.select_slider('Year', options=['2021-40', '2041-60', '2061-80', '2081-2100'], value='2100')
# dict_scen = {'ssp126': 1,
#              'ssp245': 2,
#              'ssp370': 3,
#              'ssp585': 4,
#              }

# dict_time = {'2021-2040': 1,
#              '2041-2060': 2,
#              '2061-2080': 3,
#              '2081-2100': 4,
#              }

# ## select data
# year_range = str(int(year)-19)+"-"+str(year)
# sel = dict_scen[scenario.lower()]*dict_time[year_range]-1

# ## make DF from array - select scenario
# dd = pd.DataFrame(rr[sel])
# dd = dd.iloc[:,[1,2,3,4,5]]
# dd.columns = ['lat','lon', 'mean temp/y ', 'ppt/y ', 'cluster']

# ## add info to columns
# dd['cluster_name'] = 'Cluster ' + dd['cluster'].astype(str)
# dd['ppt/y '] =  ' ' + dd['ppt/y '].astype(str) + ' mm'
# dd['mean temp/y '] = ' ' + dd['mean temp/y '].astype(str) + ' °C'

# ## plot - first trial
# fig = px.scatter(dd, x='lon', y='lat', range_x=[-5,725], range_y=[320,0],
#                  color='cluster', color_continuous_scale=px.colors.sequential.Viridis,
#                  hover_name='cluster_name',
#                  hover_data={'cluster':False,
#                            'lon':False,
#                            'lat':False,
#                            'mean temp/y ':True,
#                            'ppt/y ':True}) ## make map bigger than max range
# fig.update_layout(height=800)
# fig.update_yaxes(title='y', visible=False, showticklabels=False)
# fig.update_xaxes(title='x', visible=False, showticklabels=False)
# fig.update(layout_coloraxis_showscale=False) ## no legend
# fig.update_layout({
#     'plot_bgcolor': 'rgba(0,0,0,0)',
#     'paper_bgcolor': 'rgba(0,0,0,0)'
# }) ## background color - maybe adjust to streamlit page-s background

# fig.update_traces(
#     marker=dict(size=1.8, opacity=0.7),
#     hoverlabel = dict(bgcolor = 'red')
# )

# # Plot!
# st.plotly_chart(fig, use_container_width=True)

# ################################################################


selection_method = st.selectbox('The garden growing point selection method:', options=("latitude / longitude","address"))

if selection_method == "latitude / longitude":
    st.subheader('Insert lat/lon below:')
    input_coords()
else:
    address_text = st.text_input('Insert your address below', 'Berliner Str. 1, Mainz')
    input_coordinates = coordinates_from_address(address_text)
    input_lon = input_coordinates[0]
    input_lat = input_coordinates[1]
    st.write('The selected coordinates are:', input_lon, input_lat)

if st.button('Submit'):

    data = fetch(f"http://localhost:8000/predict?lat={input_lat}&lon={input_lon}2&ssp={scenario}&year={year}")
    if data:
        st.write("data")
    else:
        st.error("Error")


    st.header('Your garden today')
    st.subheader('Your garden today is generally populated by these species:')
    st.text("However, the red ones may have to relocate by year {year}...")
    if 'key' not in st.session_state:
        st.session_state['key'] = data['key1']
    plot_map(pd.DataFrame.from_dict(st.session_state['key'], orient='columns'), input_lat, input_lon)
