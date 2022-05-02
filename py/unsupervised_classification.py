#!/usr/bin/env python
# coding: utf-8

# # Unsupervised Machine Learning GEE

# Unsupervised classification of Landsat-8 image using Kmeans clustering.

# ### libraries

# In[2]:


import ee
import geemap


# ### Interactive Map

# In[3]:


Map = geemap.Map()
Map.setCenter(36.8, -1.3, 11)
Map


# ### Add data to map

# In[4]:


point = ee.Geometry.Point([36.9, -1.4])

image = (
    ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .filterBounds(point)
    .filterDate('2020-01-01', '2020-12-31')
    .sort('CLOUD_COVER')
    .first()
    .select('B[1-7]')
)

vis_params = {
    'min': 0,
    'max': 3000,
    'bands': ['B5', 'B4', 'B3']
}

Map.addLayer(image, vis_params, "Landsat-8")


# ### Check image properties

# In[5]:


props = geemap.image_props(image)
props.getInfo()


# ### Make trainiing dataset

# Create a region for generating training dataset.
# 1. Draw a shape.
# 2. Define Geometry
# 3. Create a buffer zone from a point
# 4. If no region is defined, it will use image footprint by default

# In[6]:


#regions
region = ee.Geometry.Point(point.buffer(10000))


# In[7]:


training = image.sample(
  **{
        #     'region': region,
        'scale': 30,
        'numPixels': 5000,
        'seed': 0,
        'geometries': True,  # Set this to False to ignore geometries
    }  
)

Map.addLayer(training, {}, 'training', False)
Map


# #### Train the clusterer

# In[8]:


#create cluster instance and train it
num_clusters = 5
clusterer = ee.Clusterer.wekaKMeans(num_clusters).train(training)


# In[9]:


#cluster the input using trained clusterer
result = image.cluster(clusterer)

#visualize the clusters with random colors.
Map.addLayer(result.randomVisualizer(), {}, 'clusters')
Map


# ### Label clusters

# In[10]:


legend_keys = ['One', 'Two', 'Three', 'Four', 'ect']
legend_colors = ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3']

#Reclassify map
result = result.remap([0, 1, 2, 3, 4], [1, 2, 3, 4, 5])

#legend colors
Map.addLayer(
    result, {'min': 1, 'max': 5, 'palette': legend_colors}, 'Labelled clusters'
)
#add legend
Map.add_legend(
    legend_keys=legend_keys, legend_colors=legend_colors, position='bottomright'
)
Map


# ### visualize

# In[11]:


print('Change layer opacity:')
cluster_layer = Map.layers[-1]
cluster_layer.interact(opacity=(0, 1, 0.1))


# ### Save to device

# In[13]:


import os

out_dir = os.path.join(os.path.expanduser('~'), 'gisData/classification/gee/unsupervised')
out_file = os.path.join(out_dir, 'cluster.tif')

geemap.ee_export_image(result, filename=out_file, scale=90)

