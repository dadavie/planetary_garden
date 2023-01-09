import streamlit as st
from popup_map import plot_map, plot_map_2, plot_map_3
from address_to_latlon.address_conversion import coordinates_from_address
import plotly.express as px
import numpy as np
import pandas as pd
import requests
from streamlit_plotly_events import plotly_events
import mapbox
import streamlit.components.v1 as components
import requests
import io

st.set_page_config(layout="wide", page_icon="🧊")

page = st.sidebar.selectbox("Go to page:", ["Climate Map", "Plant Occurrences", "Plant Species", "Clusters"])


def fetch( url):
    try:
        result = requests.get(url)
        return result.json()
    except Exception:
        return {}
# Add content to the pages
if page == "Climate Map":

    Header=st.container()
    Climate_Map =st.container()






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




    # session = requests.Session()

    with Header:
        st.title ('Welcome to our Planetary Garden 🌳')


    with Climate_Map:
        st.header('1. Climate Map')
        with st.expander("Click to access model explanations"):
            st.write("<a target='_blank' href='https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/'>CMIP6 Climate Models</a>.", unsafe_allow_html=True)
        st.subheader('Pick a future and click on a spot to see how the climate changes:')



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
        # rr = np.load('plotly_data/frontend_info_future_maps.npy', allow_pickle=True)
        response = requests.get('https://drive.google.com/uc?export=download&id=1k40QTtXleyQSlTYztBT_CACPjvkKVtWi')
        response.raise_for_status()
        rr = np.load(io.BytesIO(response.content))
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
        dd['Cluster']=dd['cluster'].map(lambda x: color_means[str(x)])
        ## plot - first trial

        @st.cache
        def plot_m ():
            fig = px.scatter(dd[:60137*4], x='lon', y='lat', range_x=[-5,725], range_y=[ 320, 0],
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
            return fig
        fig=plot_m()

        # Plot! use_container_width=True
        # st.plotly_chart(fig )
        selected_points = plotly_events(fig,click_event=True, hover_event=False)

        if selected_points:
            st.write(selected_points)
            m_input_lat = (np.interp(selected_points[0]['y'], [ 0, 360], [90, -90]))
            m_input_lon = (np.interp(selected_points[0]['x'], [0, 720], [-180, 180]))
            # data = fetch(f"http://localhost:8000/predict?lat={m_input_lat}&lon={m_input_lon}2&ssp={scenario}&year={year}")
            data=fetch(f"https://hello-00002-yuy-t7c5adl74a-ew.a.run.app/predict?lat={m_input_lat}&lon={m_input_lon}&ssp=ssp126&year={year}")
            if  not data:
                st.error("Error")
            else:
                st.subheader("Changes at (lat: {}, lon:{}) from present to year {} ({} - Scenario): ".format(m_input_lat, m_input_lon,year, scenario_selected))
                col_temp, col_precip, col_cluster= st.columns([1,1,1], gap="medium")
                col_temp.metric("Mean yearly temperature (°C):", np.round(data["key2"]["future_temp"],2), np.round(data["key2"]["future_temp"]-data["key2"]["present_temp"],2))
                col_precip.metric("Mean yearly precipitation (mm/year):", np.round(data["key2"]["future_precip"],2), np.round(data["key2"]["future_precip"]-data["key2"]["present_precip"],2))
                with col_cluster:
                    st.write("Present day cluster:", int(data['present_cluster']['actual_present_cluster']) )
                    st.write("Year", year, "cluster:", data['future_cluster']['future_cluster'])


        # ################################################################
elif page == "Plant Occurrences":
    Occurrences= st.container()
    Garden = st.container()
    with Occurrences:
        st.header("2. Plant occurrences today")
        st.subheader("Click a point on the map to see who can move in 🌱 or enter your address/coordinates below")
        st.write("Click on icons to expand!")
        components.html(plot_map_2(), height=1000)


        selection_method = st.selectbox( "Selection method", options=("address", "latitude / longitude"))

        if selection_method == "latitude / longitude":
            st.subheader('Insert lat/lon below:')
            input_lat= st.number_input('insert latitude (-90 to 90)')
            input_lon= st.number_input('insert longitude (-180 to 180)')

        else:
            st.subheader('Insert address below:')
            address_text = st.text_input('Insert your address below:', '45 Rue des Cloys, Paris')
            input_coordinates = coordinates_from_address(address_text)
            input_lon = input_coordinates[0]
            input_lat = input_coordinates[1]
            st.write('The selected coordinates are:', input_lon, input_lat)




        if st.button('Submit'):

            # data = fetch(f"http://localhost:8000/predict?lat={input_lat}&lon={input_lon}2&ssp={scenario}&year={year}")
            data=fetch(f"https://hello-00002-yuy-t7c5adl74a-ew.a.run.app/predict?lat={input_lat}&lon={input_lon}&ssp=ssp126&year=2100")
            if  not data:
                st.error("Error")
            else:

                with Garden:
                    st.title('Say hello to our newcomers!')
                    st.write("We reccommend you grow these new fellas in your garden: ")
                    # if 'key' not in st.session_state:
                    #     st.session_state['key'] = data['key1']
                    # a=pd.DataFrame.from_dict(st.session_state['key'], orient='columns')
                    a=pd.DataFrame.from_dict(data['key1'], orient='columns')
                    plot_map(a)

                    # if 'key' in st.session_state:
                    #     a=pd.DataFrame.from_dict(st.session_state['key'], orient='columns')
                    #     url="https://storage.googleapis.com/planetary"


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



                        # f_data=[('Arenaria tejedensis',[8], 1429249773),('Dendropanax lehmannii',[62], 1432620231 ),('Hakea florulenta',[55,62,72], 1821383457),('Magnolia urraoensis',[32,40], 2837700659),('Pterocarya pterocarpa',[50,55,8,42,69,37,57,26,14,45,22,23], 930740102), ('Syringa josikaea',[50, 55, 14, 69, 22, 42, 23, 37, 31, 8, 7],930741619)]

                        # for i in f_data:
                        #     col_1, col_2 = st.columns([1,1])
                        #     cont2=st.container()
                        #     with cont2:
                        #         with col_1:
                        #                 st.subheader(i[0])
                        #         with col_2:
                        #             st.image(f"{url}/{i[2]}.jpg", width=130)






elif page == "Plant Species":

    species = pd.read_csv('gs://planetary_garden_static_map/Species2.csv')
    # species = pd.read_csv("../../raw_data/Species2.csv")

    df=species.copy()
    df=df[['species', 'Cluster', 'thumbnails', 'kingdom', 'phylum', 'class',
       'order', 'family', 'genus', 'scientificName', 'verbatimScientificName']]

    df['thumbnails']=[f"https://storage.googleapis.com/planetary/{x['thumbnails']}.jpg" for i, x in df.iterrows() ]
    df = df.reindex(columns=(list([a for a in df.columns if a != 'Cluster' and a!= 'thumbnails']) +['Cluster'] + ['thumbnails'] ))
    modification_container = st.container()
    with modification_container:
        st.header('Species')
        to_filter_columns = st.multiselect("Filter species on", [ 'kingdom', 'phylum', 'class','order', 'family', 'genus', 'cluster'])

    for column in to_filter_columns:
        left, right = st.columns((1, 20))
        left.write("↳")

        if column in [ 'kingdom', 'phylum', 'class','order', 'family', 'genus']:
            user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].unique(),
                default=list(df[column].unique()),
            )
            df = df[df[column].isin(user_cat_input)]
        elif column == 'cluster':
            user_cluster_input = right.multiselect(
                f"Values for cluster",
                [0,2,6,7,8,14,15, 17, 19,20,22,23,24,26,29, 30,31,32,34,35,37,38,40,41,42,45,46,48,50,51,52,53,55,56,57,60,61,62,66,67,69,72,74],
                default=[0,2,6,7,8,14,15, 17, 19,20,22,23,24,26,29, 30,31,32,34,35,37,38,40,41,42,45,46,48,50,51,52,53,55,56,57,60,61,62,66,67,69,72,74],
            )
            res=[]
            for i,row in df.iterrows():
                h=list(map(int, row['Cluster'][1:][:-1].split(", ")))
                for j in user_cluster_input:
                    if j in h:
                        res.append(row)
                        break
            df=pd.DataFrame(res)


    pd.set_option('display.max_colwidth', -1)

    def make_clickable(val):
        return '<a target="_blank" href="{}">{}</a>'.format(val, val)

    df['thumbnails'] = df['thumbnails'].apply(make_clickable)

    st.write("Number of items:",len(df))
    df = df.to_html(escape=False)
    st.write(df, unsafe_allow_html=True)



elif page == "Clusters":
    import pandas as pd
    st.header("Clusters with respective average feature values ordered by increasing yearly avg. temp.")
    with st.expander("Click to access Key & descriptions for Climate and Soil Features"):
        st.write("<a target='_blank' href='https://www.isric.org/explore/soilgrids/faq-soilgrids'>SoilGrids</a>.", unsafe_allow_html=True)
        st.write("<a target='_blank' href='https://www.worldclim.org/data/bioclim.html'>Bioclim Variables</a>.", unsafe_allow_html=True)


    # averages = pd.read_csv("../../raw_data/2021_cluster_feature_averages.csv")
    averages = pd.read_csv('gs://planetary_garden_static_map/2021_cluster_feature_averages.csv')
    averages=averages.drop(columns=['Unnamed: 0'])
    averages.set_index('Cluster', inplace=True)
    pd.set_option('display.max_colwidth', -1)
    # averages = averages.to_html(escape=False)
    st.dataframe(averages)
    # st.write(averages, unsafe_allow_html=True)

# elif page=="Dynamic Clusters":
#     with open('exemplary_interactive_map.html', 'r') as f:
#          gif=f.read()
#     components.html(gif, height=1000)




    # # Define the center and zoom level of the map
    # center = (37.7749, -122.4194)
    # zoom = 12
    # px.set_mapbox_access_token("sk.eyJ1IjoieWxhdXJlbnQ5OCIsImEiOiJjbGM5NDM1NmMwNXRtM3FtcHhjZ3BlbHY4In0.baXZ6ZdJPhb2mERfQhPIbw")

    # # px.line_mapbox()
    # mapbox_access_token = 'sk.eyJ1IjoieWxhdXJlbnQ5OCIsImEiOiJjbGM5NDM1NmMwNXRtM3FtcHhjZ3BlbHY4In0.baXZ6ZdJPhb2mERfQhPIbw'


    # mapbox.Maps(mapbox_access_token)
    # mapbox.Maps()
    # import pydeck as pdk

    # # Create a scatterplot using Pydeck
    # view_state = pdk.ViewState(
    #     latitude=37.7749,
    #     longitude=-122.4194,
    #     zoom=12,
    # )

    # scatterplot = pdk.Layer(
    #     "ScatterplotLayer",
    #     data=[{"position": [37.7749, -122.4194]}],
    #     get_position="position",
    #     get_tooltip=["label"],
    # )

    # deck = pdk.Deck(layers=[scatterplot], initial_view_state=view_state)

    # # Display the scatterplot in Streamlit
    # st.pydeck_chart(deck)

    # import pydeck as pdk

    # layer = pdk.Layer(
    #     'HexagonLayer',
    #     UK_ACCIDENTS_DATA,
    #     get_position='[lng, lat]',
    #     auto_highlight=True,
    #     elevation_scale=50,
    #     pickable=True,
    #     elevation_range=[0, 3000],
    #     extruded=True,
    #     coverage=1)

    # Set the viewport location
    # view_state = pdk.ViewState(
    #     longitude=-122.4194,
    #     latitude=37.7749,
    #     zoom=6,
    #     min_zoom=5,
    #     max_zoom=15,
    #     pitch=40.5,
    #     bearing=-27.36)

    # # Combined all of it and render a viewport
    # r = pdk.Deck(
    #     layers=[scatterplot],
    #     initial_view_state=view_state,
    #     tooltip={
    #         'html': '<b>Elevation Value:</b> hi',
    #         'style': {
    #             'color': 'white'
    #         }
    #     }
    # )
    # st.pydeck_chart(r)





#     import streamlit.components.v1 as components

#         # bootstrap 4 collapse example
#     components.html(
#         """
#         <head>
#         <meta charset="utf-8">
#         <title>Display a popup on click</title>
#         <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
#         <link href="https://api.mapbox.com/mapbox-gl-js/v2.11.0/mapbox-gl.css" rel="stylesheet">
#         <script src="https://api.mapbox.com/mapbox-gl-js/v2.11.0/mapbox-gl.js"></script>
#         <style>
#         body { margin: 0; padding: 0; }
#         #map { position: absolute; top: 0; bottom: 0; width: 100%; }
#         </style>
#         </head>
#         <body>
#         <style>
#         .mapboxgl-popup {
#         max-width: 400px;
#         font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
#         }
#         </style>
#         <div id="map"></div>
#         <script>
#             mapboxgl.accessToken = 'sk.eyJ1IjoieWxhdXJlbnQ5OCIsImEiOiJjbGM5NDM1NmMwNXRtM3FtcHhjZ3BlbHY4In0.baXZ6ZdJPhb2mERfQhPIbw';
#         const map = new mapboxgl.Map({
#         container: 'map',
#         // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
#         style: 'mapbox://styles/mapbox/streets-v12',
#         center: [-77.04, 38.907],
#         zoom: 11.15
#         });

#         map.on('load', () => {
#         map.addSource('places', {
#         // This GeoJSON contains features that include an "icon"
#         // property. The value of the "icon" property corresponds
#         // to an image in the Mapbox Streets style's sprite.
#         'type': 'geojson',
#         'data': {
#         'type': 'FeatureCollection',
#         'features': [
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>Make it Mount Pleasant</strong><p><a href="http://www.mtpleasantdc.com/makeitmtpleasant" target="_blank" title="Opens in a new window">Make it Mount Pleasant</a> is a handmade and vintage market and afternoon of live entertainment and kids activities. 12:00-6:00 p.m.</p>',
#         'icon': 'theatre'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.038659, 38.931567]
#         }
#         },
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>Mad Men Season Five Finale Watch Party</strong><p>Head to Lounge 201 (201 Massachusetts Avenue NE) Sunday for a <a href="http://madmens5finale.eventbrite.com/" target="_blank" title="Opens in a new window">Mad Men Season Five Finale Watch Party</a>, complete with 60s costume contest, Mad Men trivia, and retro food and drink. 8:00-11:00 p.m. $10 general admission, $20 admission and two hour open bar.</p>',
#         'icon': 'theatre'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.003168, 38.894651]
#         }
#         },
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>Big Backyard Beach Bash and Wine Fest</strong><p>EatBar (2761 Washington Boulevard Arlington VA) is throwing a <a href="http://tallulaeatbar.ticketleap.com/2012beachblanket/" target="_blank" title="Opens in a new window">Big Backyard Beach Bash and Wine Fest</a> on Saturday, serving up conch fritters, fish tacos and crab sliders, and Red Apron hot dogs. 12:00-3:00 p.m. $25.grill hot dogs.</p>',
#         'icon': 'bar'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.090372, 38.881189]
#         }
#         },
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>Ballston Arts & Crafts Market</strong><p>The <a href="http://ballstonarts-craftsmarket.blogspot.com/" target="_blank" title="Opens in a new window">Ballston Arts & Crafts Market</a> sets up shop next to the Ballston metro this Saturday for the first of five dates this summer. Nearly 35 artists and crafters will be on hand selling their wares. 10:00-4:00 p.m.</p>',
#         'icon': 'art-gallery'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.111561, 38.882342]
#         }
#         },
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>Seersucker Bike Ride and Social</strong><p>Feeling dandy? Get fancy, grab your bike, and take part in this year\'s <a href="http://dandiesandquaintrelles.com/2012/04/the-seersucker-social-is-set-for-june-9th-save-the-date-and-start-planning-your-look/" target="_blank" title="Opens in a new window">Seersucker Social</a> bike ride from Dandies and Quaintrelles. After the ride enjoy a lawn party at Hillwood with jazz, cocktails, paper hat-making, and more. 11:00-7:00 p.m.</p>',
#         'icon': 'bicycle'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.052477, 38.943951]
#         }
#         },
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>Capital Pride Parade</strong><p>The annual <a href="http://www.capitalpride.org/parade" target="_blank" title="Opens in a new window">Capital Pride Parade</a> makes its way through Dupont this Saturday. 4:30 p.m. Free.</p>',
#         'icon': 'rocket'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.043444, 38.909664]
#         }
#         },
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>Muhsinah</strong><p>Jazz-influenced hip hop artist <a href="http://www.muhsinah.com" target="_blank" title="Opens in a new window">Muhsinah</a> plays the <a href="http://www.blackcatdc.com">Black Cat</a> (1811 14th Street NW) tonight with <a href="http://www.exitclov.com" target="_blank" title="Opens in a new window">Exit Clov</a> and <a href="http://godsilla.bandcamp.com" target="_blank" title="Opens in a new window">Gods’illa</a>. 9:00 p.m. $12.</p>',
#         'icon': 'music'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.031706, 38.914581]
#         }
#         },
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>A Little Night Music</strong><p>The Arlington Players\' production of Stephen Sondheim\'s  <a href="http://www.thearlingtonplayers.org/drupal-6.20/node/4661/show" target="_blank" title="Opens in a new window"><em>A Little Night Music</em></a> comes to the Kogod Cradle at The Mead Center for American Theater (1101 6th Street SW) this weekend and next. 8:00 p.m.</p>',
#         'icon': 'music'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.020945, 38.878241]
#         }
#         },
#         {
#         'type': 'Feature',
#         'properties': {
#         'description':
#         '<strong>Truckeroo</strong><p><a href="http://www.truckeroodc.com/www/" target="_blank">Truckeroo</a> brings dozens of food trucks, live music, and games to half and M Street SE (across from Navy Yard Metro Station) today from 11:00 a.m. to 11:00 p.m.</p>',
#         'icon': 'music'
#         },
#         'geometry': {
#         'type': 'Point',
#         'coordinates': [-77.007481, 38.876516]
#         }
#         }
#         ]
#         }
#         });
#         // Add a layer showing the places.
#         map.addLayer({
#         'id': 'places',
#         'type': 'symbol',
#         'source': 'places',
#         'layout': {
#         'icon-image': ['get', 'icon'],
#         'icon-allow-overlap': true
#         }
#         });

#         // When a click event occurs on a feature in the places layer, open a popup at the
#         // location of the feature, with description HTML from its properties.
#         map.on('click', 'places', (e) => {
#         // Copy coordinates array.
#         const coordinates = e.features[0].geometry.coordinates.slice();
#         const description = e.features[0].properties.description;

#         // Ensure that if the map is zoomed out such that multiple
#         // copies of the feature are visible, the popup appears
#         // over the copy being pointed to.
#         while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
#         coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
#         }

#         new mapboxgl.Popup()
#         .setLngLat(coordinates)
#         .setHTML(description)
#         .addTo(map);
#         });

#         // Change the cursor to a pointer when the mouse is over the places layer.
#         map.on('mouseenter', 'places', () => {
#         map.getCanvas().style.cursor = 'pointer';
#         });

#         // Change it back to a pointer when it leaves.
#         map.on('mouseleave', 'places', () => {
#         map.getCanvas().style.cursor = '';
#         });
#         });
#         </script>

#         </body>
#     """
#     ,
#     height=600,
# )












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





        #   with Garden:
        #         st.title('Inspection of your garden today')
        #         st.header('Your garden today is generally populated by these species:')
        #         st.header('The average temperature here is 10°C and precipitation is 838mm/year, Cluster #70')


        #         if 'key' not in st.session_state:
        #             st.session_state['key'] = data['key1']
        #         a=pd.DataFrame.from_dict(st.session_state['key'], orient='columns')
        #         plot_map(a)
        #         # st.header (f" However, the red ones may have to relocate by year {year}...")

        #     # with Moving_out:
        #         st.title(f"Our garden environment in {year}")
        #         st.header ('The climate has changed here (on average +5°C and -114mm precip/year), conditions similar to present day Cluster #10')
        #         st.title("Moving out")
        #         st.header(f"The RED species may have to move out by year {year}")



            #    with Moving_in:

            #         st.title("Moving in")
            #         st.header(f"Say hello to your planetary garden newcomers! These species may well thrive in the climate of your garden in {year}:")
