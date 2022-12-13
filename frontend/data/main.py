import streamlit as st
from popup_map import plot_map

st.set_page_config(layout="wide")

Header=st.container()
Climate_Map =st.container()
Garden = st.container()
Moving_Out = st.container()
Moving_In = st.container()

st.markdown(
    """
    <style>
    .main {
    background-color: #cbed9f ;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def input_coords():
    input_lat= st.number_input('insert latitude (-90 to 90)')
    input_lon=st.number_input('insert longitude (-180 to 180)')
    return input_lat, input_lon

with Header:
    st.title ('Welcome to our Planetary Garden')


with Climate_Map:
    st.header('Climate Map')
    st.subheader('Select climate future for your garden:')
    map_col, slider_col= st.columns(2)
    map_col.text("MAP")
    scenario = slider_col.selectbox('Climate Scenario', options=['SSP4563', 'SSP3547', 'SSP483y8g'], index=2)
    year = slider_col.select_slider('Year', options=['2040', '2060', '2080', '2100'], value='2100')
    no_clusters = slider_col.select_slider('Number of clusters', options=['20', '30', '60', '100'], value='60')

    st.subheader('Select a point on the map where you want to grow your garden...or insert your address/ or lat/lon below:')
    input_coords()

with Garden:
    st.header('Your garden today')
    plot_map()
    st.subheader('Your garden today is generally populated by these species:')
    st.text("However, the red ones may have to relocate by year ___...")


with Moving_Out:
    st.header("Moving out")
    st.text('These species may have to move out by year ___ :( ')
    st.text ('The climate has changed here (on average 1 degreee, and > 6mm3 precip for e.g) and may not be suitable for these species anymore')




with Moving_In:
    st.header("Moving in")
    st.text('Say hello to your planetary garden newcommers!')
