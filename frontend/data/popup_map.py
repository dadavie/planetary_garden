import streamlit as st
# from streamlit_folium import st_folium
from streamlit_folium import folium_static
import folium
import os
import base64
from PIL import Image
import requests
import io


def plot_map(df, lat, lon):
    points=[[lat+0.5, lon+0.5], [lat+1, lon+1], [lat-1, lon-0.92], [lat-0.87, lon+0.97], [lat+1, lon-1], [lat-0.24, lon-0.5],[lat+0.32, lon-0.6],[lat-0.56, lon+0.78],[lat-0.13, lon-0.1],[lat+0.89, lon-0.34], [lat-0.8, lon+0.6], [lat+0.02, lon-0.3], [lat-0.75, lon-0.74], [lat+0.15, lon+0.56], [lat-0.4, lon+0.56], [lat+1, lon+1]]
    map = folium.Map(location=[lat, lon], zoom_start=9, tiles="Stamen Terrain", width=1200, height=900)

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
        folium.vector_layers.Marker(location=points[i],popup = popup,icon= folium.Icon(color=color, icon_color='black',icon = 'globe', sticky=True)).add_to(map)

    st_data = folium_static(map, width = 1200, height =900)


#st_folium

            # <center>
            #     <img src="{full_filename}" width="200" style="border-radius: 50px;"/>
            # </center>


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
