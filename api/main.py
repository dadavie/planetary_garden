from fastapi import FastAPI
from get_current_plants_from_latlon import *
import json

app=FastAPI()


@app.get("/predict")
def predict (lat=None, lon=None, ssp=None, year=None):
    lat=float(lat)
    lon=float(lon)
    year=int(year)
    a, b, c, d, e= parse_df(lat, lon, ssp, year)
    return { 'key1':a, 'key2':b, 'key3':c, 'present_cluster':d, 'future_cluster':e}

def parse_df(lat, lon, ssp, year):
    present_cluster=get_future_cluster(lat, lon, 'ssp126', 2040)
    future_cluster=get_future_cluster(lat, lon, ssp, year)
    a,b = get_lists( present_cluster, future_cluster)
    c = get_difference(present_cluster, future_cluster)
    res_a = a.to_json(orient="records")
    res_b = b.to_json(orient="records")
    parsed_a = json.loads(res_a)
    parsed_b = json.loads(res_b)
    return parsed_a, parsed_b, c, present_cluster, future_cluster

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
