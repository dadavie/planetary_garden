import pandas as pd
import numpy as np
import random



def get_plants (lat, lon):
        data=pd.read_csv('../raw_data/2021.csv')
        ct_lat = int(round(np.interp(lat, [-90, 90], [360, 0])))
        ct_lon = int(round(np.interp(lon, [-180, 180], [0, 720])))
        for i, row in data.iterrows():
            if row['1']==ct_lat and row['2']==ct_lon:

                return row['future_cluster']
        return ValueError('No climate data')


def get_future_cluster(lat, lon, ssp, year):
    future=np.load("../raw_data/future_scenarios_lonlat_clusters_new.npy")
    if ssp == "ssp126":
        sp=0
    elif ssp == "ssp245":
        sp=1
    elif ssp == "ssp370":
        sp=2
    elif ssp == "ssp585":
        sp=3
    else:
        sp=np.nan

    if year ==2040:
        yr=0
    elif year == 2060:
        yr=1
    elif year == 2080:
        yr=2
    elif year == 2100:
        yr=3
    else:
        yr=np.nan
    loc=4*sp+ yr
    ct_lat = int(round(np.interp(lat, [-90, 90], [360, 0])))
    ct_lon = int(round(np.interp(lon, [-180, 180], [0, 720])))
    for i in range(len(future[0])):
         if future[loc,i,1]==ct_lat and future[loc,i,2]==ct_lon:
            return future[loc,i,3]
    return ValueError('No future climate data')

# def get_lists (present_cluster, future_cluster):
#     species=pd.read_csv("../raw_data/Species.csv")
#     pres=[]
#     recom=[]
#     for i, row in species.iterrows():
#         h = list(map(int, row['Cluster'][1:][:-1].split(", ")))
#         o=0
#         for j in h:
#             if j == present_cluster:
#                 o=1
#                 pres.append(row[['species','Cluster','at_risk', 'thumbnails']])
#                 pres[-1]['Cluster']=h
#                 for k in h:
#                     if k == future_cluster:
#                         pres[-1].loc ['at_risk']=0

#         if o==0:
#             for g in h:
#                 if g== future_cluster:
#                     recom.append(row[['species','Cluster', 'at_risk', 'thumbnails']])
#     if (len(pres)>6):
#         pres=random.sample(pres, 6)
#     if (len(recom)>7):
#         recom=random.sample(recom, 7)
#     return pd.DataFrame(pres), pd.DataFrame(recom)

def get_lists (present_cluster, future_cluster):
    species=pd.read_csv("../raw_data/Species.csv")
    pres=[]
    recom=[]
    for i, row in species.iterrows():
        h = list(map(int, row['Cluster'][1:][:-1].split(", ")))
        o=0
        for j in h:
            if j == present_cluster:
                o=1
                pres.append(row[['species','Cluster','at_risk', 'thumbnails']])
                pres[-1]['Cluster']=h
                for k in h:
                    if k == future_cluster:
                        pres[-1].loc ['at_risk']=0
                        break

        if o==0:
            for g in h:
                if g== future_cluster:
                    recom.append(row[['species','Cluster', 'at_risk', 'thumbnails']])
    if (len(pres)>12):
        pres=random.sample(pres, 12)
    if (len(recom)>12):
        recom=random.sample(recom, 12)
    return pd.DataFrame(pres), pd.DataFrame(recom)

a,b= get_lists(get_plants(46.904053, 17.822115), get_future_cluster(46.904053, 17.822115, 'ssp585', 2040))

print(b.shape)

def get_difference (present_cluster, future_cluster):
    data=pd.read_csv("../raw_data/mean_temps.csv")
    present_temp=None
    present_precip=None
    future_temp=None
    future_precip=None
    for i, row in data.iterrows():
        if row['cluster']==present_cluster:
            present_temp=row['mean temp/y']
            present_precip=row['ppt/y ']
        if row['cluster']==future_cluster:
            future_temp=row['mean temp/y']
            future_precip=row['ppt/y ']

    dictt= {
        'present_temp':present_temp,
        'present_precip':present_precip,
        'future_temp':future_temp,
        'future_precip':future_precip
     }
    return dictt
