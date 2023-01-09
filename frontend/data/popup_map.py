import streamlit as st
# from streamlit_folium import st_folium
from streamlit_folium import st_folium, folium_static
import folium
import os
import base64
from PIL import Image
import requests
import io
import pandas as pd
from folium.plugins import FastMarkerCluster, MarkerCluster
import leafmap.foliumap



def plot_map(df):
    # points=[[lat+0.5, lon+0.5], [lat+1, lon+1], [lat-1, lon-1.92], [lat-0.87, lon+0.97], [lat+1, lon-1], [lat-2.24, lon-0.5],[lat+0.32, lon-0.6],[lat-0.56, lon+0.78],[lat-0.13, lon-0.1],[lat+1.89, lon-0.34], [lat-0.8, lon+0.6], [lat+2.72, lon-0.3], [lat-0.75, lon-0.74], [lat+0.15, lon+0.56], [lat-0.4, lon+0.56], [lat+1, lon+1]]

    map = folium.Map(location=[30, -7], zoom_start=3, tiles="Stamen Terrain", width=1200, height=700)

    # file_ = open("../static/photos/butterfly.jpg", "rb")
    # contents = file_.read()
    # data_url = base64.b64encode(contents).decode("utf-8")
    # file_.close()
    #file_=open(f"../static/photos/{i[0]}.jpg", "rb")
    #file_=open(f"https://storage.googleapis.com/planetary/{i[0]}.jpg", "rb")

    # dictt =  {0:'red',
    #         1: 'red',
    #         2: 'red',
    #         3: 'green',
    #         4: 'red',
    #         5: 'green',
    #         6: 'red',
    #         7: 'green',
    #         8:  'red',
    #         9: 'red',
    #         10:'green',
    #         11:'red',
    #         12:'red',
    #         13:'red',
    #         14:'green',
    #         15:'red'

    #               }
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
                <h7><b> {row['species']} </b></p>
                                <center>
                    <img src="data:image/jpg;base64,{data_url}" width="90" style="border-radius: 20px;"/>
                </center>
<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'>Phylum: {row['phylum']}<br>Class: {row['class']}<br>Order: {row['order']}<br>Family: {row['family']}<br>Genus: {row['genus']}<br><b>Species: {row['species']}</b><br>Cluster: {row['Cluster']}<br></div>


        </html>

        """, script=True)

        # color='red'
        # html = folium.Html(
        #         f"""
        #         <!DOCTYPE html>
        #         <html>
        #         <h7> <b> {row['species']}</b>; Relocate to: {str(row['Cluster'])[1:-1]} </p>

        #         <center>
        #             <img src="data:image/jpg;base64,{data_url}" width="80" style="border-radius: 50px;"/>
        #         </center>
        #     <center>
        #         <img src="{full_filename}" width="200" style="border-radius: 50px;"/>
        #     </center>

        # </html>

        # """, script=True)

        popup  = folium.Popup(html, max_width=130, max_height= 130, show=True)

        folium.vector_layers.Marker(location=[row['lat'], row['lon']], popup=popup,icon= folium.Icon(color='green', icon_color='black',icon = 'globe', sticky=True)).add_to(map)
        # folium.vector_layers.Marker(location=points[i],popup = popup,icon= folium.Icon(color='green', icon_color='black',icon = 'globe', sticky=True)).add_to(map)
    html2=folium.Html(      f"""
                <!DOCTYPE html>
                <html>
                <h7><b> YOUR GARDEN HERE! </b></p>

        </html>

        """, script=True)
    popup_garden=folium.Popup(html2, max_width=160, max_height= 160, show=True)
    folium.vector_layers.Marker(location=[df.iloc[0]['lat_ref'], df.iloc[0]['lon_ref']], popup=popup_garden,icon= folium.Icon(color='pink', icon_color='black',icon = 'leaf', sticky=True)).add_to(map)
    st_data = folium_static(map, width = 1200, height =700)


#st_folium



        # html = folium.Html(
        #         f"""
        #         <!DOCTYPE html>
        #         <html>
        #         <h1 align="center" style="font-family:Calibri; color:white"><strong><u>Species name</u><strong>
        #         <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        #         <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
        #         </h1>
        #         <!-- <p class="narrow" style="text-align: left;"> -->
        #         <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">

        #             <div class="panel panel-default" style="text-align: left; border-color: #ffffff !important;">
        #                 <div class="panel-heading" role="tab" id="headingOne" style="background: #ffffff!important;">
        #                     <h4 class="panel-title" style="color:cornflowerblue">
        #                         <a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
        #                             <strong> <i class="fa fa-newspaper-o"></i> {i[0]} <span class="glyphicon glyphicon-menu-down" aria-hidden="true" style="float: right;"></span></strong>
        #                         </a>
        #                     </h4>
        #                 </div>
        #                 <div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">
        #                     <div class="panel-body" align="justify">
        #                     At risk
        #                     </div>
        #                 </div>
        #             </div>

        #         <center>
        #             <img src="data:image/jpg;base64,{data_url}" width="50" style="border-radius: 50px;"/>
        #         </center>


        #         </div>

        # </html>

@st.cache
def plot_map_2():
    # points=[[lat+0.5, lon+0.5], [lat+1, lon+1], [lat-1, lon-1.92], [lat-0.87, lon+0.97], [lat+1, lon-1], [lat-2.24, lon-0.5],[lat+0.32, lon-0.6],[lat-0.56, lon+0.78],[lat-0.13, lon-0.1],[lat+1.89, lon-0.34], [lat-0.8, lon+0.6], [lat+2.72, lon-0.3], [lat-0.75, lon-0.74], [lat+0.15, lon+0.56], [lat-0.4, lon+0.56], [lat+1, lon+1]]
    # map = folium.Map(location=[15, 73], zoom_start=3, tiles="Stamen Terrain", width=1200, height=900)
    # df= pd.read_csv("../../raw_data/occurrences.csv")

    # for i,row in df[:50].iterrows():
    #     # url = f"https://storage.googleapis.com/planetary/{row['thumbnails_x']}.jpg"
    #     # response = requests.get(url)
    #     # img = Image.open(io.BytesIO(response.content))
    #     # img.save("tmp.jpg")
    #     # file_= open("tmp.jpg", "rb")
    #     # contents = file_.read()
    #     # data_url = base64.b64encode(contents).decode("utf-8")
    #     # file_.close()
    #     color='green'
    #     html = folium.Html(
    #             f"""
    #             <!DOCTYPE html>
    #             <html>
    #             <h7> <b> {row['species']}</b>; Location: Cluster {row['Cluster_x']}; Relocate to: {str(row['Cluster_y'])[1:-1]} </p>
    #     </html>

    #     """, script=True)

    #     popup  = folium.Popup(html, max_width=130, max_height= 130, show=True)
    #     folium.vector_layers.Marker(location=[row['decimalLatitude'], row['decimalLongitude']],popup = popup,icon= folium.Icon(color=color, icon_color='black',icon = 'globe', sticky=True)).add_to(map)
    # df2=df[:200]
    # map.add_child(FastMarkerCluster(df2[['decimalLatitude', 'decimalLongitude']].values.tolist()))








                # <center>
                #     <img src="data:image/jpg;base64,{data_url}" width="80" style="border-radius: 50px;"/>
                # </center>
    # points=[[lat+0.5, lon+0.5], [lat+1, lon+1], [lat-1, lon-1.92], [lat-0.87, lon+0.97], [lat+1, lon-1], [lat-2.24, lon-0.5],[lat+0.32, lon-0.6],[lat-0.56, lon+0.78],[lat-0.13, lon-0.1],[lat+1.89, lon-0.34], [lat-0.8, lon+0.6], [lat+2.72, lon-0.3], [lat-0.75, lon-0.74], [lat+0.15, lon+0.56], [lat-0.4, lon+0.56], [lat+1, lon+1]]


#     f = folium.Figure(width=1000, height=500)
#     map = folium.Map(location=[25.2, -0.28], zoom_start=10, width=1200, height=900).add_to(f)
# # tiles="Stamen Terrain",
# # 'var markerCluster = new MarkerClusterer(map, markers, {maxZoom: 4, minimumClusterSize: 10, gridSize: 60});'
    # callback = ('function (row) {'
    #                 'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
    #                 'var icon = L.AwesomeMarkers.icon({'
    #                 "icon: 'leaf',"
    #                 "iconColor: 'white',"
    #                 "markerColor: 'green',"
    #                 "prefix: 'glyphicon',"
    #                 "extraClasses: 'fa-rotate-0'"
    #                     '});'
    #                 'marker.setIcon(icon);'
    #                 "var popup = L.popup({maxWidth: '300'});"
    #                 "const display_text = {text: row[2]};"
    #                 "var mytext = $(' <div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> ${row[2]}</div>')[0];"
    #                 "popup.setContent(mytext);"
    #                 "marker.bindPopup(popup);"
    #                 'return marker};')

    #<img src='https://storage.googleapis.com/planetary/1123124019.jpg' width='200' style='border-radius: 50px;'/>

    # #  ${dfshort['speices']}
    # fgv = folium.FeatureGroup(name="Cluster38")

    # # loop through and plot everything
    # df38=df[df['Cluster_x']==38]
    # dfshort=df38[:5]
    # fgv.add_child(FastMarkerCluster(dfshort[['decimalLatitude', 'decimalLongitude']].values.tolist(), callback=callback, control=True, name="cluster38", overlay=True))


    # fps = folium.FeatureGroup(name="Cluster45")
    # df45=df[df['Cluster_x']==45]
    # dfshortt=df45[:10]
    # fps.add_child(FastMarkerCluster(dfshortt[['decimalLatitude', 'decimalLongitude']].values.tolist(), callback=callback, control=True, name="cluster45", overlay=True))


    # map.add_child(fgv)
    # map.add_child(fps)
    # folium.LayerControl(position='bottomright').add_to(map)


    # Map=st.container()

    # with Map:
    # import streamlit.components.v1 as components
    # #st_data =st_folium(map, width=725)
    # selections = st.multiselect("Choose clusters", df.Cluster_x.unique())
    # all_options = st.checkbox("Select all options")

    # if all_options:
    #     selections = df.Cluster_x.unique()

    # m = folium.Map(location=[39.949610, -75.150282], zoom_start=2, tiles="Stamen Terrain", width=2000, height=900)
    # for s in selections:
    #     fgm=folium.FeatureGroup(name=f"Cluster{s}")
    #     dfx=df[df['Cluster_x']==s]
    #     dfshortt=dfx
    #     fgm.add_child(FastMarkerCluster(dfshortt[['decimalLatitude', 'decimalLongitude','species', 'thumbnails_x']].values.tolist(), callback=callback, control=True, name=f"Cluster{s}", overlay=True))
    #     m.add_child(fgm)
    # layer_control = folium.LayerControl()
    # layer_control.add_to(m)
    # # foliumap.add_layer_control(m)
    # st_data = st_folium(m, width=725)



    # m.add_child(fgv)
    # map.add_child(fps)
    # call to render Folium map in Streamlit



    with open('../../notebooks/ignore_yolanda/map4.html', 'r') as f:
         map=f.read()
    # components.iframe('https://storage.cloud.google.com/planetary_garden_static_map/map2.html', height=900)
    # return components.html(map, height=600,)
    # components.iframe("https://storage.cloud.google.com/planetary_garden_static_map/map2.html", height=900)
    return map
#colors['40']['r'], colors['40']['g'], colors['40']['b']

def plot_map_3(a):


    callback = ( 'function (row) {'
        'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
        'var icon = L.AwesomeMarkers.icon({'
        "icon: 'leaf',"
        "iconColor: 'white',"
        "markerColor: 'green',"
        "prefix: 'glyphicon',"
        "extraClasses: 'fa-rotate-0'"
            '});'
        "marker.setIcon(icon);"
        "var popup = L.popup({maxWidth: '300'});"
        "const display_text = {text: row[2]};var mytext = $(`<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'>Phylum: ${row[3]}<br>Class: ${row[4]}<br>Order: ${row[5]}<br>Family: ${row[6]}<br>Genus: ${row[7]}<br><b>Species: ${row[2]}</b><br>Cluster: ${row[8]}<br><img src='https://storage.googleapis.com/planetary/${row[9]}.jpg' width='100' style='border-radius: 10px;'/></div>`)[0];"
        "popup.setContent(mytext);marker.bindPopup(popup);"
        'return marker};;')
    m = folium.Map(location=[39.949610, -7], zoom_start=2, tiles="Stamen Terrain", width=1200, height=900)
    fgm=folium.FeatureGroup(name="group")
    fgm.add_child(FastMarkerCluster(a[['lat', 'lon','species','phylum','class','order','family','genus', 'Cluster', 'thumbnails']].values.tolist(), callback=callback, min_cluster_size=20))
    m.add_child(fgm)

    st_data = folium_static(m, width = 1200, height =700)

        # 'var icon = L.ExtraMarkers.icon({'
        # "icon: 'fa-leaf',"
        # "markerColor: '#4287f5',"
        # "shape: 'circle',"
        # "prefix: 'fa',"
        # "svg:'True'"
        # '});"'




        # callback = ('function (row) {'
    #                 'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
    #                 'var icon = L.AwesomeMarkers.icon({'
    #                 "icon: 'leaf',"
    #                 "iconColor: 'white',"
    #                 "markerColor: 'green',"
    #                 "prefix: 'glyphicon',"
    #                 "extraClasses: 'fa-rotate-0'"
    #                     '});'
    #                 'marker.setIcon(icon);'
    #                 "var popup = L.popup({maxWidth: '300'});"
    #                 "const display_text = {text: row[2]};"
    #                 "var mytext = $(' <div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> ${row[2]}</div>')[0];"
    #                 "popup.setContent(mytext);"
    #                 "marker.bindPopup(popup);"
    #                 'return marker};')
