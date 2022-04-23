#!/usr/bin/env python
# coding: utf-8

# Libraries

# In[20]:


#import earthengine_api
import geemap
import ee


# In[12]:


ee.Authenticate()


# In[14]:


ee.Initialize()


# In[28]:


Map = geemap.Map(center = (40, -100), zoom = 4)
Map


# Add EarthEngine data

# In[26]:


#load earth engine datasets
dem = ee.Image('USGS/SRTMGL1_003')
landcover = ee.Image("ESA/GLOBCOVER_L4_200901_200912_V2_3").select('landcover')
landsat7 = ee.Image('LE7_TOA_5YEAR/1999_2003')
states = ee.FeatureCollection('TIGER/2018/States')


# Set Visualization Parameters

# In[17]:


dem_vis = {
'min': 0,
'max': 4000,
'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}

landsat_vis = {
    'min': 20,
    'max': 200,
    'bands': ['B4', 'B3', 'B2']
}


# Display data on Map

# In[24]:


Map.addLayer(dem, dem_vis, 'SRTM DEM', True, 0.5)
Map.addLayer(landcover, {}, 'Land Cover')
Map.addLayer(landsat7, landsat_vis, 'Landsat 7')
Map.addLayer(states, {}, "US States")

