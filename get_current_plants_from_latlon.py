import pandas as pd
import numpy as np
def get_current_plants (lat, lon):
    res=[]
    c_lat = int(round(np.interp(lat, [-90, 90], [0, 360])))
    # c_lat_right=c_lat+1
    c_lon = int(round(np.interp(lon, [-180, 180], [0, 720])))
    # c_lon_right=c_lon+1
    occurences=pd.read_csv('raw_data/RedFlag_occurences_alldata_inklClusters.csv')
    # print (occurences.head())
    for i, row in occurences.iterrows():
        llat=row['decimalLatitude']
        llon=row['decimalLongitude']
        ct_lat = int(round(np.interp(llat, [-90, 90], [0, 360])))
        ct_lon = int(round(np.interp(llon, [-180, 180], [0, 720])))
        # if ct_lat > c_lat & ct_lat< c_lat_right & ct_lon > c_lon & ct_lon < c_lon_right:
        if ct_lat == c_lat & ct_lon== c_lon:
            res.append(row)

    return res


h=get_current_plants(47.144379, 14.527587)
print( h, "length =", len(h))
