import streamlit as st
from popup_map import plot_map
from address_to_latlon.address_conversion import coordinates_from_address
import plotly.express as px
import numpy as np
import pandas as pd
import requests


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
    st.subheader('Pick a future to see whether your garden will survive:')
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
    year_selected = year_slider_col.select_slider('Year', options=['2021-2040', '2041-2060', '2061-2080', '2081-2100'], value='2081-2100')
    # no_clusters = slider_col.select_slider('Number of clusters', options=['20', '30', '60', '100'], value='60')

    dict_year = {'2021-2040': 2040,
             '2041-2060': 2060,
             '2061-2080': 2080,
             '2081-2100': 2100,
             }
    year=dict_year[year_selected]

    # Plotly stuff
    rr = np.load('plotly_data/frontend_info_future_maps.npy', allow_pickle=True)
    ## input from streamlit slider
    #scenario = slider_col.selectbox('Climate Scenario', options=['SSP126', 'SSP245', 'SSP370', 'SSP585'], index=2)
    #year = slider_col.select_slider('Year', options=['2021-40', '2041-60', '2061-80', '2081-2100'], value='2100')
    dict_scen = {'ssp126': 1,
                'ssp245': 2,
                'ssp370': 3,
                'ssp585': 4,
                }

    dict_time = {'2021-2040': 1,
                '2041-2060': 2,
                '2061-2080': 3,
                '2081-2100': 4,
                }

    ## select data
    year_range = str(int(year)-19)+"-"+str(year)
    sel = dict_scen[scenario.lower()]*dict_time[year_range]-1

    ## make DF from array - select scenario
    dd = pd.DataFrame(rr[sel])
    dd = dd.iloc[:,[1,2,3,4,5]]
    dd.columns = ['lat','lon', 'mean temp/y ', 'ppt/y ', 'cluster']

    ## add info to columns
    dd['cluster_name'] = 'Cluster ' + dd['cluster'].astype(str)
    dd['ppt/y '] =  ' ' + dd['ppt/y '].astype(str) + ' mm'
    dd['mean temp/y '] = ' ' + dd['mean temp/y '].astype(str) + ' °C'

    ## plot - first trial
    fig = px.scatter(dd, x='lon', y='lat', range_x=[-5,725], range_y=[320,0],
                    color='cluster', color_continuous_scale=px.colors.sequential.Viridis,
                    hover_name='cluster_name',
                    hover_data={'cluster':False,
                            'lon':False,
                            'lat':False,
                            'mean temp/y ':True,
                            'ppt/y ':True}) ## make map bigger than max range
    fig.update_layout(height=700, width=1000)
    fig.update_yaxes(title='y', visible=False, showticklabels=False)
    fig.update_xaxes(title='x', visible=False, showticklabels=False)
    fig.update(layout_coloraxis_showscale=False) ## no legend
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    }) ## background color - maybe adjust to streamlit page-s background

    fig.update_traces(
        marker=dict(size=1.8, opacity=0.7),
        hoverlabel = dict(bgcolor = 'red')
    )

    # Plot!
    st.plotly_chart(fig, use_container_width=True)

    # ################################################################

    st.header("Choose where to grow your garden:")
    selection_method = st.selectbox( "Selection method", options=("address", "latitude / longitude"))

    if selection_method == "latitude / longitude":
        st.subheader('Insert lat/lon below:')
        input_coords()
    else:
        st.subheader('Insert address below:')
        address_text = st.text_input('Insert your address below:', 'Berliner Str. 1, Mainz')
        input_coordinates = coordinates_from_address(address_text)
        input_lon = input_coordinates[0]
        input_lat = input_coordinates[1]
        st.write('The selected coordinates are:', input_lon, input_lat)

    if st.button('Submit'):

        data = fetch(f"http://localhost:8000/predict?lat={input_lat}&lon={input_lon}2&ssp={scenario}&year={year}")
        if data:
            st.write(" ")
        else:
            st.error("Error")

        with Garden:
            st.title('Inspection of your garden today')
            st.header('Your garden today is generally populated by these species:')
            st.subheader (f" However, the red ones may have to relocate by year {year}...")

            if 'key' not in st.session_state:
                st.session_state['key'] = data['key1']
            a=pd.DataFrame.from_dict(st.session_state['key'], orient='columns')
            plot_map(a, input_lat, input_lon)




        with Moving_Out:
            st.title("Moving out")
            st.header(f"These species may have to move out by year {year} :( ")
            st.subheader ('The climate has changed here (on average 1 degreee, and > 6mm3 precip for e.g) and may not be suitable for these species anymore')

            if 'key' in st.session_state:
                a=pd.DataFrame.from_dict(st.session_state['key'], orient='columns')
                url="https://storage.googleapis.com/planetary"


                for i, row in a.iterrows():
                    if row['at_risk']==1:
                        col_1, col_2 = st.columns([1,1])
                        cont=st.container()
                        with cont:
                            with col_1:
                                st.subheader(row['species'])
                            with col_2:
                                st.image(f"{url}/{row['thumbnails']}.jpg", width=150)





        with Moving_In:
            st.title("Moving in")
            st.header('Say hello to your planetary garden newcomers!')
            data["key2"]
