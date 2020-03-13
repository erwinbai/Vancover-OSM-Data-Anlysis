#!/usr/bin/env python
# coding: utf-8

# In[1]:


from xml.dom.minidom import parse, parseString
import pandas as pd
import numpy as np
import sys
import math
from pykalman import KalmanFilter


# In[2]:


data1 = pd.read_json('amenities-vancouver.json.gz', lines=True)
data1 = data1.dropna().reset_index(drop=True)
data2 = pd.read_csv('Airbnb_datalist.csv')
data3 = pd.read_csv('photo.csv')


# In[3]:


unique = data1.groupby('amenity').count()
# unique


# In[4]:


unique = unique.loc[unique['lat']==1].reset_index()
# unique


# In[5]:


unique = unique.loc[:,['amenity', 'lat']]
unique = unique.rename(columns = {'lat':'number'}).reset_index()
# unique

tmp = pd.DataFrame()
for i in unique['amenity']:
    tmp1 = data1.loc[data1['amenity'] == i]
    tmp = pd.concat([tmp, tmp1])
tmp.reset_index(drop=True)
unique = tmp[['lat', 'lon', 'amenity', 'name']]
unique = unique.reset_index(drop = True)
unique = unique.reset_index()
# unique


# In[6]:


path = data3.reset_index()
path['name'] = 'NaN'
# path


# In[7]:


earth = 6378
m = (1 / ((2 * math.pi / 360) * earth)) / 1000
for i in path['index']:
    for j in unique['index']:
        tmp_lon = path['lon'][i]
        tmp_lat = path['lat'][i]
        x1 = tmp_lon + ((500 * m)/math.cos(tmp_lat*(math.pi/180)))
        y1 = tmp_lat + (500 * m)  
        x2 = tmp_lon - ((500 * m)/math.cos(tmp_lat*(math.pi/180)))
        y2 = tmp_lat - (500 * m)
        if unique['lon'][j] < x1 and unique['lon'][j] > x2 and unique['lat'][j] < y1 and unique['lat'][j] > y2:
            if path['name'][i] == 'NaN':
                path['name'] = unique['name'][[j]]
#                 print(unique['name'][[j]])


# In[8]:


# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(path)


# In[9]:


special = path.dropna()
# special


# In[18]:


# https://www.zhihu.com/question/33783546/answer/775946401
import folium
import pandas as pd

# define the world map
world_map = folium.Map()

# display world map
world_map

latitude = 49.27128
longitude = -122.92335

# Create map and display it
van_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Display the map of San Francisco
van_map

incidents = folium.map.FeatureGroup()

# add pop-up text to each marker on the map
latitudes = list(special.lat)
longitudes = list(special.lon)
labels = list(special.name)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(van_map)
    
# latitudes = list(path.lat)
# longitudes = list(path.lon)
# labels = list(path.name)

points =[(i,j) for i,j in path.loc[:,["lat","lon"]].values.tolist()]

folium.PolyLine(points, color = 'red').add_to(van_map)

    
# add incidents to map
van_map.add_child(incidents)


# In[ ]:




