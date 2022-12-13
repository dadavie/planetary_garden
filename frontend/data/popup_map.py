import streamlit as st
from streamlit_folium import st_folium
import folium
import os
import base64





def plot_map():

    plant_ids=(['butterfly',[38.58, -99.09]], ['snake',[32.58, -95.09]], ['elephant', [29.58, -90.09]])
    map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain", width=1300, height=700)

    # file_ = open("../static/photos/butterfly.jpg", "rb")
    # contents = file_.read()
    # data_url = base64.b64encode(contents).decode("utf-8")
    # file_.close()

    for i in plant_ids:
        coords=i[1]
        file_=open(f"../static/photos/{i[0]}.jpg", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        html = folium.Html(
                f"""
                <!DOCTYPE html>
                <html>
                <p> {i[0]} </p>

                <center>
                    <img src="data:image/jpg;base64,{data_url}" width="70" style="border-radius: 50px;"/>
                </center>

        </html>

        """, script=True)

        popup  = folium.Popup(html, max_width=120, max_height= 120, show=True)
        folium.vector_layers.Marker(location=i[1],popup = popup,icon= folium.Icon(color='beige', icon_color='yellow',icon = 'globe')).add_to(map)

    st_data = st_folium(map, width = 1525)




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
