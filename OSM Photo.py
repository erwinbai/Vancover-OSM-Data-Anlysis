#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image

X = "HCKK0512.JPEG"


# In[2]:


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

exif = get_exif(X)
print(exif)


# In[3]:


from PIL.ExifTags import TAGS

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

exif = get_exif(X)
labeled = get_labeled_exif(exif)
print(labeled)


# In[4]:


from PIL.ExifTags import GPSTAGS

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

exif = get_exif(X)
geotags = get_geotagging(exif)
#print(geotags)-122.90839


# In[5]:


def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)
def get_time(geotags):
    time = geotags['GPSDateStamp']
    return(time)


# In[6]:


exif = get_exif(X)
geotags = get_geotagging(exif)
print(get_coordinates(geotags))


# In[7]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
from math import cos, asin, sqrt, pi
data = pd.read_csv("photo.csv")
data


# In[8]:


# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
#The below code for caculation of two points is Edited by Alexander Volkov, Answered by Salvador Dali 
def distance_between_points(lat1, lon1, lat2, lon2):
    p = pi/180     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) *  (1 - cos((lon2 - lon1) * p)) / 2
    
    return 12742 * asin(sqrt(a))
distance_for_points = np.vectorize(distance_between_points)


# In[9]:


def distance(output1):
    output1['distance']=distance_for_points(output1['lat'],output1['lon'],output1['lat'].shift(periods=-1),output1['lon'].shift(periods=-1));
    dis = output1['distance'].sum()
    
    del output1['distance']
    return dis * 1000


# In[ ]:





# In[10]:


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1,   trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


# In[11]:


print("Total distance travled: " + str(distance(data)) + " meter")
output_gpx(data, 'out.gpx')


# In[ ]:




