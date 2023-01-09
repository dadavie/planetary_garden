import pandas as pd
import numpy as np
import random
import joblib
import requests
import io
from sklearn.cluster import KMeans



def get_plants (lat, lon):
        # data=pd.read_csv('../raw_data/2021.csv')
        data = pd.read_csv('gs://planetary_garden_static_map/2021.csv')
        ct_lat = int(round(np.interp(lat, [-90, 90], [360, 0])))
        ct_lon = int(round(np.interp(lon, [-180, 180], [0, 720])))
        for i, row in data.iterrows():
            if row['1']==ct_lat and row['2']==ct_lon:

                return row['future_cluster']
        return ValueError('No climate data')


def get_future_cluster(lat, lon, ssp, year):
    # future=np.load("../raw_data/future_scenarios_lonlat_clusters_new.npy")
    response = requests.get('https://storage.googleapis.com/planetary_garden_static_map/future_scenarios_lonlat_clusters_new.npy')
    response.raise_for_status()
    future = np.load(io.BytesIO(response.content))

    # future = np.load('gs://planetary_garden_static_map/future_scenarios_lonlat_clusters_new.npy')
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
            return int(future[loc,i,3])
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
#                         break

#         if o==0:
#             for g in h:
#                 if g== future_cluster:
#                     recom.append(row[['species','Cluster', 'at_risk', 'thumbnails']])
#     if (len(pres)>12):
#         pres=random.sample(pres, 12)
#     if (len(recom)>12):
#         recom=random.sample(recom, 12)
#     return pd.DataFrame(pres), pd.DataFrame(recom)

# a,b= get_lists(get_plants(46.904053, 17.822115), get_future_cluster(46.904053, 17.822115, 'ssp585', 2040))

# print(b.shape)

def get_difference (present_cluster, future_cluster):
    # data=pd.read_csv("../raw_data/mean_temps.csv")
    data = pd.read_csv('gs://planetary_garden_static_map/mean_temps.csv')
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

def get_features (lat, lon):
        # present=pd.read_csv('../raw_data/2021.csv')
        present = pd.read_csv('gs://planetary_garden_static_map/2021.csv')
        ct_lat = int(round(np.interp(lat, [-90, 90], [360, 0])))
        ct_lon = int(round(np.interp(lon, [-180, 180], [0, 720])))
        for i, row in present.iterrows():
           if row['1']==ct_lat and row['2']==ct_lon:
               scaler = joblib.load("scaler.save")
               df=pd.DataFrame(row[4:-1]).T
               df.columns=['b1', 'b2',
       'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13',
       'b14', 'b15', 'b16', 'b17', 'b18', 'b19', 'sg1', 'sg2', 'sg3', 'sg4',
       'sg5', 'sg6', 'sg7', 'sg8', 'sg9', 'sg10', 'sg11', 'sg12', 'sg13',
       'sg14', 'sg15', 'sg16', 'sg17', 'sg18', 'sg19', 'sg20', 'sg21', 'sg22',
       'sg23', 'sg24', 'sg25', 'sg26', 'sg27', 'sg28', 'sg29', 'sg30', 'sg31',
       'sg32', 'sg33', 'sg34', 'sg35', 'sg36', 'sg37', 'sg38', 'sg39', 'sg40',
       'sg41', 'sg42', 'sg43', 'sg44', 'sg45', 'sg46', 'sg47', 'sg48', 'sg49',
       'sg50', 'sg51', 'sg52', 'sg53', 'sg54', 'sg55', 'sg56', 'sg57', 'sg58',
       'sg59', 'sg60']
               df=scaler.transform(df)

               return df
        # return ValueError('No climate data')



def prediction (clus, lat, lon):
    # data=pd.read_csv("../raw_data/RedFlag_species_alldata_inkl_futureCL_inklClusters_with_thumbnails.csv")
    data = pd.read_csv('gs://planetary_garden_static_map/RedFlag_species_alldata_inkl_futureCL_inklClusters_with_thumbnails.csv')
    data_strings=data[[ 'Unnamed: 0','kingdom',
       'phylum','class','order','family','genus','species',
       'scientificName','verbatimScientificName','countryCode','locality',
       'stateProvince','decimalLatitude', 'decimalLongitude','year','red_flag','Cluster', 'thumbnails']]
    f=[]
    kmean=joblib.load("kmeans_model.sav")
    for i in range(len(kmean.labels_)):
        if kmean.labels_[i]==clus[0]:
            f.append(i)
    df=pd.DataFrame(f)
    df['species']=[data_strings.iloc[i].loc['species']for i in f]
    df['lon']=[data_strings.iloc[i].loc['decimalLongitude']for i in f]
    df['lat']=[data_strings.iloc[i].loc['decimalLatitude']for i in f]
    df['lon_ref']=[lon for i in f]
    df['lat_ref']=[lat for i in f]
    df['lon_dif']=(df['lon_ref']-df['lon'])**2
    df['lat_dif']=(df['lat_ref']-df['lat'])**2
    df['sum']=df['lon_dif']+df['lat_dif']
    df['phylum']=[data_strings.iloc[i].loc['phylum']for i in f]
    df['class']=[data_strings.iloc[i].loc['class']for i in f]
    df['order']=[data_strings.iloc[i].loc['order']for i in f]
    df['family']=[data_strings.iloc[i].loc['family']for i in f]
    df['genus']=[data_strings.iloc[i].loc['genus']for i in f]
    df['thumbnails']=[data_strings.iloc[i].loc['thumbnails']for i in f]
    df['Cluster']=[data_strings.iloc[i].loc['Cluster']for i in f]
    df=df.sort_values(by=['sum'])
    length=int(df.shape[0]/70)
    df=df[-length:]
    df=df.sample(30).sort_values(by=['sum'], ascending=False)
    df=df.drop_duplicates(subset=['species'])
    return df

def return_reccommendation (lat, lon):
    model=joblib.load("kmeans_model.sav")
    return prediction(model.predict(get_features(lat,lon)),lat, lon)
