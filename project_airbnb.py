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


# In[3]:


# data1


# In[4]:


need = 'not_na'
# needs_ame = []
needs_nam = []
# while need != 'NaN':
#     need = input('What you need nearby your hotel? (enter name or NaN) ')
# #     if need in data1['amenity'].values:
# #         needs_ame.append(need)
#     if need in data1['name'].values:
#         needs_nam.append(need)
#     elif need == 'NaN':
#         print('Thank you for your information.')
#     else:
#         print('Sorry! Cannot find ' + need + '. ')

needs_nam.append('KFC')
needs_nam.append('Starbucks')
needs_nam.append('Subway')
# needs_nam


# In[5]:


# for i in needs:
#     if i in data1['name'].values:
#         print(i)
#     if i in data1['amenity'].values:
#         print(i)


# In[6]:


# if 'cafe' in data1['amenity'].values:
#     print('cafe')


# In[7]:


tmp = pd.DataFrame()
# for i in needs_ame:
#     tmp1 = data1.loc[data1['amenity'] == i]
#     tmp = pd.concat([tmp, tmp1])
for j in needs_nam:
    tmp2 = data1.loc[data1['name'] == j]
    tmp = pd.concat([tmp, tmp2])
needs_data = tmp.reset_index(drop = True)


# In[8]:


# tmp1 = data1.loc[data1['name'] == 'Starbucks']
# tmp2 = data1.loc[data1['name'] == 'Salad Loop']
# tmp = pd.concat([tmp1, tmp2]).reset_index(drop = True)


# In[9]:


# needs_data


# In[10]:


data2 = data2.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
data2['lat'] = data2['lat'].astype(float)
data2['lon'] = data2['lon'].astype(float)
# data2


# In[11]:


data2 = data2.loc[data2['room_type'] == 'Hotel room'].reset_index(drop = True)
# data2


# In[12]:


# lon_range = '(' + str(data2['lon'].min()) + ' to ' + str(data2['lon'].max()) + ')'
# lat_range = '(' + str(data2['lat'].min()) + ' to ' + str(data2['lat'].max()) + ')'
# initial_lon = input('Please enter your longitude to finde nearby hotel. ' + lon_range + ' ')
# initial_lat = input('Please enter your latitude to finde nearby hotel. ' + lat_range + ' ')
# initial_lon = float(initial_lon)
# initial_lat = float(initial_lat)

initial_lat = 49.2823254
initial_lon = -123.1187994


# In[13]:


# print(type(initial_lon))


# In[14]:


earth = 6378
m = (1 / ((2 * math.pi / 360) * earth)) / 1000

#https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters
# initial_lon = np.random.uniform(data2['lon'].min(), data2['lon'].max())
#print(initial_lon)
# initial_lat = np.random.uniform(data2['lat'].min(), data2['lat'].max())
#print(initial_lat)

x1 = initial_lon + ((5000 * m)/math.cos(initial_lat*(math.pi/180)))
y1 = initial_lat + (5000 * m)  

x2 = initial_lon - ((5000 * m)/math.cos(initial_lat*(math.pi/180)))
y2 = initial_lat - (5000 * m)

hotel_range = data2.loc[data2['lon'] < x1].reset_index(drop=True)
hotel_range = hotel_range.loc[hotel_range['lon'] > x2]
hotel_range = hotel_range.loc[hotel_range['lat'] < y1]
hotel_range = hotel_range.loc[hotel_range['lat'] > y2]
hotel_range = hotel_range.reset_index(drop=True)


# In[15]:


# price_range = '(' + str(hotel_range['price'].min()) + ' to ' + str(hotel_range['price'].max()) + ')'
# min_price = input('What is the min price of the hotel you want? ' + price_range + ' ')
# max_price = input('What is the max price of the hotel you want? ' + price_range + ' ')
# min_price = int(min_price)
# max_price = int(max_price)


min_price = 60
max_price = 500


# In[16]:


# print(type(max_price))


# In[17]:


hotel_range = hotel_range.loc[hotel_range['price'] < max_price]
hotel_range = hotel_range.loc[hotel_range['price'] > min_price]
hotel_data = hotel_range.reset_index(drop = True)


# In[18]:


# empty = []
for i in range(len(needs_nam)):
#     print(needs_nam[i])
#     name = 'KFC'
#     hotel_data[name] = 0
    hotel_data[needs_nam[i]] = 0
# hotel_data


# In[19]:


hotel_data = hotel_data.reset_index()
# hotel_data


# In[20]:


needs_data = needs_data.reset_index()
# needs_data


# In[21]:


for i in hotel_data['index']:
    for j in needs_data['index']:
        tmp_lon = hotel_data['lon'][i]
        tmp_lat = hotel_data['lat'][i]
        x1 = tmp_lon + ((500 * m)/math.cos(tmp_lat*(math.pi/180)))
        y1 = tmp_lat + (500 * m)  
        x2 = tmp_lon - ((500 * m)/math.cos(tmp_lat*(math.pi/180)))
        y2 = tmp_lat - (500 * m)
        if needs_data['lon'][j] < x1 and needs_data['lon'][j] > x2 and needs_data['lat'][j] < y1 and needs_data['lat'][j] > y2:
            hotel_data[needs_data['name'][j]][i] = hotel_data[needs_data['name'][j]][i] + 1


# In[22]:


# tmp_lat = 49.2823254
# tmp_lon = -123.1187994
# x1 = tmp_lon + ((5000 * m)/math.cos(tmp_lat*(math.pi/180)))
# y1 = tmp_lat + (5000 * m)  
# x2 = tmp_lon - ((5000 * m)/math.cos(tmp_lat*(math.pi/180)))
# y2 = tmp_lat - (5000 * m)
# print(x1)
# print(y1)
# print(x2)
# print(y2)
# print(needs_data['lon'][394])
# print(hotel_data[needs_data['name'][1]][1])
# print('--------')
# for j in needs_data['index']:
#     print(j)
#     if needs_data['lon'][j] < x1 and needs_data['lon'][j] > x2 and needs_data['lat'][j] < y1 and needs_data['lat'][j] > y2:
#         print('find!!!!!!')
#          hotel_data[needs_data['name'][j]][i] = hotel_data[needs_data['name'][j]][i] + 1


# In[23]:


# hotel_data


# In[24]:


hotel_data = hotel_data.loc[hotel_data['KFC']>0]
hotel_data = hotel_data.loc[hotel_data['Starbucks']>0]
hotel_data = hotel_data.loc[hotel_data['Subway']>0]
hotel_data = hotel_data.drop(columns = ['index'])
hotel_data.reset_index(drop = True)


# In[25]:


# https://www.zhihu.com/question/33783546/answer/775946401
import folium
import pandas as pd

# define the world map
world_map = folium.Map()

# display world map
world_map

latitude = 49.2823254
longitude = -123.1187994

# Create map and display it
van_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Display the map of San Francisco
van_map

incidents = folium.map.FeatureGroup()

# add pop-up text to each marker on the map
latitudes = list(hotel_data.lat)
longitudes = list(hotel_data.lon)
labels = list(hotel_data.name)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(van_map)
    
# latitudes = list(needs_data.lat)
# longitudes = list(needs_data.lon)
# labels = list(needs_data.name)

# for lat, lng, label in zip(latitudes, longitudes, labels):
#     folium.Marker([lat, lng], popup=label).add_to(van_map)  
    
# add incidents to map
van_map.add_child(incidents)


# In[26]:


from folium.plugins import HeatMap

# let's start again with a clean copy of the map of San Francisco
san_map = folium.Map(location = [latitude, longitude], zoom_start = 12)

# Convert data format
heatdata = needs_data[['lat','lon']].values.tolist()

# add incidents to map
HeatMap(heatdata).add_to(van_map)

van_map

