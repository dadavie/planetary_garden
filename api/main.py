from fastapi import FastAPI
from get_current_plants_from_latlon import *
import json





app=FastAPI()


@app.get("/predict")
def predict (lat=None, lon=None, ssp=None, year=None):
    lat=float(lat)
    lon=float(lon)
    year=int(year)
    a, b, c, d = parse_df(lat, lon, ssp, year)
    json_data = { 'key1':a, 'key2':b, 'present_cluster':c, 'future_cluster':d}
    return json_data

def parse_df(lat, lon, ssp, year):
    actual_present_cluster=get_plants(lat, lon)
    present_cluster=get_future_cluster(lat, lon, 'ssp126', 2040)
    future_cluster=get_future_cluster(lat, lon, ssp, year)
    a=return_reccommendation (lat, lon)
    b = get_difference(present_cluster, future_cluster)
    res_a = a.to_json(orient="records")
    parsed_a = json.loads(res_a)
    pres_clust_dict = { 'present_cluster':present_cluster, 'actual_present_cluster':actual_present_cluster}
    fut_clust_dict ={ 'future_cluster':future_cluster}
    return parsed_a, b, pres_clust_dict, fut_clust_dict



# old parse_df:
# def parse_df(lat, lon, ssp, year):
#     actual_present_cluster=get_plants(lat, lon)
#     present_cluster=get_future_cluster(lat, lon, 'ssp126', 2040)
#     future_cluster=get_future_cluster(lat, lon, ssp, year)
#     a,b = get_lists( actual_present_cluster, future_cluster)
#     c = get_difference(present_cluster, future_cluster)
#     res_a = a.to_json(orient="records")
#     res_b = b.to_json(orient="records")
#     parsed_a = json.loads(res_a)
#     parsed_b = json.loads(res_b)
#     pres_clust_dict = { 'present_cluster':present_cluster, 'actual_present_cluster':actual_present_cluster}
#     fut_clust_dict ={ 'future_cluster':future_cluster}
#     return parsed_a, parsed_b, c, pres_clust_dict, fut_clust_dict




# @app.get("/questions")
# def load_questions():
#     return parse_df(df)




# from fastapi import FastAPI


# app= FastAPI()

# @app.get('/')
# def index():
#     return{'value': 'Go to https://math-api-cd-4zunylksjq-uc.a.run.app/docs' }
# #this is a change

# @app.get('/multiply')
# def multiply(a,b):
#     return{'result': int(a)*int(b)}

# @app.get('/substract')
# def substract(a,b):

#     return{'result': int(a)-int(b)}

# @app.get('/sum')
# def multiply(a,b):
#     return{'result': int(a)+int(b)}
