## https://stackoverflow.com/questions/58032813/displaying-image-on-folium-marker-pop-up

## https://github.com/python-visualization/folium/pull/778
## https://discuss.streamlit.io/t/set-map-dimentions-for-folium-static/22789

# class Popup(Element):

#     def __init__(self, html=None, parse_html=False, max_width=300, default_open=False):

#         ### unchanged code removed ###

#         self.default_open = default_open

#         self._template = Template(u"""
#             var {{this.get_name()}} = L.popup({maxWidth: '{{this.max_width}}'});
#             {% for name, element in this.html._children.items() %}
#                 var {{name}} = $('{{element.render(**kwargs).replace('\\n',' ')}}')[0];
#                 {{this.get_name()}}.setContent({{name}});
#             {% endfor %}
#             {{this._parent.get_name()}}.bindPopup({{this.get_name()}})
#             {% if this.default_open %}.openPopup(){% endif %};
#             {% for name, element in this.script._children.items() %}
#                 {{element.render()}}
#             {% endfor %}
#         """)  # noqa

import folium
from folium import IFrame

import os

from folium.plugins import FloatImage
from flask import Flask, render_template



import numpy as np
import branca

import base64
import matplotlib.pyplot as plt



import pandas as pd

import imageio



app = Flask(__name__)


FOLDER = os.path.join('static', 'photos')

app.config['UPLOAD_FOLDER'] = FOLDER






@app.route('/')
def index():
    start_coords = (46.9540700, 142.7360300)
    map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain", width=1300, height=700)
    # folium_map = folium.Map(location=start_coords, zoom_start=14)


    # try:
    ## # add img to popup
    # file =  'butterfly.png'
    # dir_base = os.getcwd()
    # Filename = dir_base + "/" + file
    # encoded = base64.b64encode(open(Filename, 'rb').read())
    # html = '<img src="data:image/png;base64,{}'.format

    # """
    # <object data="data:image/png;base64,{}" width="{}" height="{} type="image/svg+xml">
    # </object>""".format


    #     html="""
    # <iframe src=\"""" + df_final['html_file'][i] + """\" width="850" height="400"  frameborder="0">
    # """

    # popup = folium.Popup(folium.Html(html, script=True))


    # width, height, fat_wh = 2200, 2200, 1.3
    # iframe = IFrame(html(encoded.decode('UTF-8'), width+20, height+20) , width=width*fat_wh, height=height*fat_wh)
    # popup  = folium.Popup(iframe,parse_html = True, max_width=3000)

##45.464, 9.1915

    # except (FileNotFoundError, NameError) as error:
    #      print( "no dir given .. ")




#   width, height, fat_wh = 300, 300, 1.3
# Adding this to the iframe:

#   iframe = IFrame(svg(encoded.decode('UTF-8'), width, height) , width=width*fat_wh, height=height*fat_wh)
# Adding iframe to popup:

#   popup  = folium.Popup(iframe, parse_html = True, max_width=1500)
# Adding popup to Marker and Marker to map m :

#   folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']],  icon=folium.Icon(color='brown', icon='anchor', prefix='fa'),
#                 popup=popup).add_to(m)




    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'butterfly.jpg')

    html = folium.Html(
            f"""
            <!DOCTYPE html>
            <html>
            <h1 align="center" style="font-family:Calibri; color:white"><strong><u>Species name</u><strong>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
            </h1>
            <!-- <p class="narrow" style="text-align: left;"> -->
            <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">

                <div class="panel panel-default" style="text-align: left; border-color: #ffffff !important;">
                    <div class="panel-heading" role="tab" id="headingOne" style="background: #ffffff!important;">
                        <h4 class="panel-title" style="color:cornflowerblue">
                            <a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                                <strong> <i class="fa fa-newspaper-o"></i> About <span class="glyphicon glyphicon-menu-down" aria-hidden="true" style="float: right;"></span></strong>
                            </a>
                        </h4>
                    </div>
                    <div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">
                        <div class="panel-body" align="justify">
                        At risk
                        </div>
                    </div>
                </div>




            </div>

            <center>
                <img src="{full_filename}" width="200" style="border-radius: 50px;"/>
            </center>
    </html>

    """, script=True)


    popup  = folium.Popup(html, max_width=200, show=True)
    folium.vector_layers.Marker(location=[38.58, -99.09],popup = popup,icon= folium.Icon(color='beige', icon_color='yellow',icon = 'globe')).add_to(map)


            ##folium.Marker(location=[38.58, -99.09],popup = popup).add_to(map)

            ##,tooltip=str(row['Name'])





    return map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
