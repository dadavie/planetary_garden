import streamlit as st
from popup_map import plot_map
from address_to_latlon.address_conversion import coordinates_from_address
import plotly.express as px
import numpy as np
import pandas as pd
import requests
from streamlit_plotly_events import plotly_events


st.set_page_config(layout="wide", page_icon="🧊")

Header=st.container()
Climate_Map =st.container()
Garden = st.container()
Moving_out=st.container()
Moving_in= st.container()




# st.markdown(
#     """
#     <style>
#     .main {
#     background-color: #d8ed9d ;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )



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
    dd = pd.DataFrame(rr[sel])
    dd = dd.iloc[:,[1,2,3,4,5]]
    dd.columns = ['lat','lon', 'mean temp/y ', 'ppt/y ', 'cluster']

    ## add info to columns
    dd['cluster_name'] = 'Cluster ' + dd['cluster'].astype(str)
    dd['ppt/y '] =  ' ' + dd['ppt/y '].astype(str) + ' mm'
    dd['mean temp/y '] = ' ' + dd['mean temp/y '].astype(str) + ' °C'


    ## add info to columns
    dd['cluster_name'] = 'Cluster ' + dd['cluster'].astype(str)
    dd['ppt/y '] =  ' ' + dd['ppt/y '].astype(str) + ' mm'
    dd['mean temp/y '] = ' ' + dd['mean temp/y '].astype(str) + ' °C'

    color_means={ '16':1,'49':2,'63':3,'47':4,'73':5,'5':6,'65':7,'36':8,'20':9,'42':10,'30':11,'46':12,'11':13,'54':14,'27':15,'1':16,'52':17,'44':18,'17':19,'0':20,'10':21,'9':22,'59':23,'25':24,'70':25,'18':26,'33':27,'58':28,'21':29,'3':30,'13':31,'12':32,'28':33,'39':34,'43':35,'4':36,'64':37}
    dd['cluster_ordered_by_temp']=dd['cluster'].map(lambda x: color_means[str(x)])
    ## plot - first trial
    fig = fig = px.scatter(dd[:60137*4], x='lon', y='lat', range_x=[-5,725], range_y=[320,0],
                    color='cluster_ordered_by_temp', color_continuous_scale=px.colors.sequential.Turbo,
                    hover_name='cluster_name',
                    hover_data={'cluster':False,
                            'lon':False,
                            'lat':False,
                            'mean temp/y ':True,
                            'ppt/y ':True}) ## make map bigger than max range
    fig.update_layout(height=600, width=1200)
    fig.update_yaxes(title='y', visible=False, showticklabels=False)
    fig.update_xaxes(title='x', visible=False, showticklabels=False)
    fig.update(layout_coloraxis_showscale=False) ## no legend
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    }) ## background color - maybe adjust to streamlit page-s background

    fig.update_traces(
        marker=dict(size=2.5, opacity=0.7),
        hoverlabel = dict(bgcolor = 'red')
    )

    # Plot! use_container_width=True
    # st.plotly_chart(fig )
    selected_points = plotly_events(fig,click_event=True, hover_event=False)
    if selected_points:
        st.write(selected_points)
        input_lat=selected_points[0]['x']
        input_lon=selected_points[0]['y']

    # ################################################################

    st.header("Choose where to grow your garden:")
    selection_method = st.selectbox( "Selection method", options=("address", "latitude / longitude"))

    if selection_method == "latitude / longitude":
        st.subheader('Insert lat/lon below:')
        input_lat= st.number_input('insert latitude (-90 to 90)')
        input_lon= st.number_input('insert longitude (-180 to 180)')

    else:
        st.subheader('Insert address below:')
        address_text = st.text_input('Insert your address below:', 'Berliner Str. 1, Mainz')
        input_coordinates = coordinates_from_address(address_text)
        input_lon = input_coordinates[0]
        input_lat = input_coordinates[1]
        st.write('The selected coordinates are:', input_lon, input_lat)

    if st.button('Submit') or selected_points:


        data = fetch(f"http://localhost:8000/predict?lat={input_lat}&lon={input_lon}2&ssp={scenario}&year={year}")
        if data:
            st.write(" ")
        else:
            st.error("Error")

        with Garden:
            st.title('Inspection of your garden today')
            st.header('Your garden today is generally populated by these species:')
            st.header('The average temperature here is 10°C and precipitation is 838mm/year, Cluster #70')


            if 'key' not in st.session_state:
                st.session_state['key'] = data['key1']
            a=pd.DataFrame.from_dict(st.session_state['key'], orient='columns')
            plot_map(a, input_lat, input_lon)
            # st.header (f" However, the red ones may have to relocate by year {year}...")

        # with Moving_out:
            st.title(f"Our garden environment in {year}")
            st.header ('The climate has changed here (on average +5°C and -114mm precip/year), conditions similar to present day Cluster #10')
            st.title("Moving out")
            st.header(f"The RED species may have to move out by year {year}")


            if 'key' in st.session_state:
                a=pd.DataFrame.from_dict(st.session_state['key'], orient='columns')
                url="https://storage.googleapis.com/planetary"


                # for i, row in a.iterrows():
                #     if row['at_risk']==1:
                #         col_1, col_2 = st.columns([1,1])
                #         cont=st.container()
                #         with cont:
                #             with col_1:
                #                 st.subheader(row['species'])
                #                 st.text(f"Relocate to cluster(s): {row['Cluster']}")
                #             with col_2:
                #                 st.image(f"{url}/{row['thumbnails']}.jpg", width=130)


            with Moving_in:

                st.title("Moving in")
                st.header(f"Say hello to your planetary garden newcomers! These species may well thrive in the climate of your garden in {year}:")
                # f_data=[('Arenaria tejedensis',[8], 1429249773),('Dendropanax lehmannii',[62], 1432620231 ),('Hakea florulenta',[55,62,72], 1821383457),('Magnolia urraoensis',[32,40], 2837700659),('Pterocarya pterocarpa',[50,55,8,42,69,37,57,26,14,45,22,23], 930740102), ('Syringa josikaea',[50, 55, 14, 69, 22, 42, 23, 37, 31, 8, 7],930741619)]

                # for i in f_data:
                #     col_1, col_2 = st.columns([1,1])
                #     cont2=st.container()
                #     with cont2:
                #         with col_1:
                #                 st.subheader(i[0])
                #         with col_2:
                #             st.image(f"{url}/{i[2]}.jpg", width=130)

                st.write(data['key2'])
                st.write(data['key3'])
                st.write(data['present_cluster'])
                st.write(data['future_cluster'])


    #  with Future:
    #         go=st.container()
    #         with go:
    #             st.title(f"Our garden in {year}")
    #             c1,c2=st.columns([1,1])

    #             c1.title("Moving out")
    #             c1.header(f"These species may have to move out by year {year}")
    #             c1.subheader('The climate has changed here (on average > 4 degrees celsius) and may not be suitable for these species anymore')
    #             c2.title("Moving in")
    #             c2.header('Say hello to your planetary garden newcomers!')

    #         next=st.container()
    #         with next:
    #             left_col_1, left_col_2, right_col_1, right_col_2=next.columns([1,1,1,1])


    #             if 'key' in st.session_state:
    #                 a=pd.DataFrame.from_dict(st.session_state['key'], orient='columns')
    #                 url="https://storage.googleapis.com/planetary"
    #                 for i, row in a.iterrows():
    #                     if row['at_risk']==1:
    #                         # left_col_1, left_col_2 = st.columns([1,1])
    #                         cont=st.container()
    #                         with cont:
    #                             left_col_1.subheader(row['species'])
    #                             left_col_2.image(f"{url}/{row['thumbnails']}.jpg", width=150)







# ## make DF from array - select scenario
#     dd = pd.DataFrame(rr[sel])
#     dd = dd.iloc[:,[1,2,3,4,5]]
#     dd.columns = ['lat','lon', 'mean temp/y ', 'ppt/y ', 'cluster']

#     ## add info to columns
#     dd['cluster_name'] = 'Cluster ' + dd['cluster'].astype(str)
#     dd['ppt/y '] =  ' ' + dd['ppt/y '].astype(str) + ' mm'
#     dd['mean temp/y '] = ' ' + dd['mean temp/y '].astype(str) + ' °C'

#     color_means={ '16':1,'49':2,'63':3,'47':4,'73':5,'5':6,'65':7,'36':8,'20':9,'42':10,'30':11,'46':12,'11':13,'54':14,'27':15,'1':16,'52':17,'44':18,'17':19,'0':20,'10':21,'9':22,'59':23,'25':24,'70':25,'18':26,'33':27,'58':28,'21':29,'3':30,'13':31,'12':32,'28':33,'39':34,'43':35,'4':36,'64':37}
#     dd['cluster_ordered_by_temp']=dd['cluster'].map(lambda x: color_means[str(x)])
#     ## plot - first trial
#     fig = fig = px.scatter(dd, x='lon', y='lat', range_x=[-5,725], range_y=[320,0],
#                     color='cluster_ordered_by_temp', color_continuous_scale=px.colors.sequential.Turbo,
#                     hover_name='cluster_name',
#                     hover_data={'cluster':False,
#                             'lon':False,
#                             'lat':False,
#                             'mean temp/y ':True,
#                             'ppt/y ':True}) ## make map bigger than max range
#     fig.update_layout(height=600, width=1200)
#     fig.update_yaxes(title='y', visible=False, showticklabels=False)
#     fig.update_xaxes(title='x', visible=False, showticklabels=False)
#     fig.update(layout_coloraxis_showscale=False) ## no legend
#     fig.update_layout({
#         'plot_bgcolor': 'rgba(0,0,0,0)',
#         'paper_bgcolor': 'rgba(0,0,0,0)'
#     }) ## background color - maybe adjust to streamlit page-s background

#     fig.update_traces(
#         marker=dict(size=2.5, opacity=0.7),
#         hoverlabel = dict(bgcolor = 'red')
#     )

#     # Plot! use_container_width=True
#     st.plotly_chart(fig )
#     # selected_points = plotly_events(fig,click_event=True, hover_event=False)
#     # st.write(selected_points)
