#!/usr/bin/env python
# coding: utf-8

# # Landsat Timelapse Nairobi

# ## libraries

# In[2]:


import geemap
import os
import ee


# ## Interactive map

# In[73]:


Map = geemap.Map()
Map.setCenter(36.9, -1.5, 10)
Map


# In[59]:


##roi = Map.draw_last_feature


# ## Landsat timelapse

# In[60]:


out_dir = os.path.join(os.path.expanduser("~"), 'gisData/timelapse')
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


# In[61]:


label = 'Urban Growth in Nairobi'
nai_gif =Map.add_landsat_ts_gif(
    label=label,
    start_year=1995,
    bands=['Red', 'Green', 'Blue'],
    font_color='white',
    frames_per_second=10,
    progress_bar_color='blue',
)

