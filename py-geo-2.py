#%%
# ENVIRONMENT SETUP ----

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import geopandas
# import shapely
# import pysal 
#  the pysal metapackage doesnt actually contain any code, 
    # just a set of dependencies on its constituent subpackages. 
# Chances are good you don't actually need everything in the metapackage, 
# so you could also install the subpackages you are looking to use directly
# import fiona
# import pyproj
import pyrosm
# import osmnx
# import matplotlib
import os
# conda install -c conda-forge folium matplotlib mapclassify
from dash import Dash, dcc, html
import dash_leaflet
import json


os.getcwd()
# os.chdir("C:/Users/John TH Wong/Documents")
# os.chdir("/Users/john/Library/Mobile Documents/com~Apple~CloudDocs/research/coding/py-geo")
def wd(): 
    return os.getcwd()
wd = wd()

# %% 
# CSDI PORTAL DATA ----

df_openspace = geopandas.read_file("data/POS.json") # Public Open Space
df_dist_boundaries = geopandas.read_file("data/DCD.json") # District Council Boundaries

# %%
df_openspace.head()
df_dist_boundaries.head()
#%%
df_openspace = df_a.drop(columns = 'LASTUPDATE')
df_openspace.explore()
df_dist_boundaries.explore()

# %%
# OPENSTREETMAP DATA ----

fp = pyrosm.get_data("test_pbf")

# %%
fp_1 = pyrosm.get_data("Amsterdam")
#%%
osm = pyrosm.OSM(fp_1)
# %%
buildings = osm.get_buildings()
# buildings.plot()
# len(buildings)
# buildings.explore()
#%%
buildings.plot()

# %%
# pyrosm.data.sources.available.keys()
pyrosm.data.sources.cities.available
pyrosm.data.sources.subregions.available.keys()
pyrosm.data.sources.asia.available

#%%
help(pyrosm.OSM)

# %%
buildings.crs
buildings_3067 = buildings.to_crs(epsg = 3067)
buildings_3067.plot()

# extracts the geometry of the first-indexed in the buildings object 
geom = buildings.loc[0, "geometry"]
geom_3067 = buildings_3067.loc[0, "geometry"]
# geom
geom_3067
type(geom_3067)
type(buildings)

# %%
buildings_3067.area
buildings_3067.area.describe()

# %%
# osm is an object defined earlier.
# get_pois stands for get points of interests
restaurants = osm.get_pois(custom_filter = {'amenity': ['restaurant']} )

# %%
restaurants.plot()

# %%
# this merges buildings to observations of restautrants, 
    # where the two intersect
# the predicate argument, unused below, defaults to intersects; 
    # others include contains, crosses, etc.
# .sjoin_nearest() joins based on "closest", 
    # with max distance set by user, rather than "touching"
# overlay() keeps both rather than merges
# .sjoin can be called from both geopandas package and GeoDataFrames objects
join = geopandas.sjoin(buildings, restaurants, how = 'inner')

# %%
join.plot()
# %% 
buildings.describe()
buildings
buildings.columns
type(buildings['geometry'])
# overlay = geopandas.overlay(restaurants, buildings, 
#                             how = 'intersection', keep_geom_type = False)

# %%
roads = osm.get_network()
# %%
plot = join.plot(column = 'building_left', figsize = (12,12), cmap = 'RdYlBu', 
                 legend = True)
plot = roads.plot(edgecolor = 'gray', linewidth = 0.75,
                 # this argument aligns the roads.plot with the plot object 
                     # from previous line
                ax = plot 
                )
plot.set_ylim([52.36, 52.38])
plot.set_xlim([4.88, 4.91])


# %%
# CSDI PORTAL DATA 2 ----

df_hk_buildings = geopandas.read_file('data/building_FSDT/BUILDING_STRUCTURE.json')
# %%
df_hk_buildings.plot()
# %%
# df_hk_buildings.describe()
df_hk_buildings.columns
# df_hk_buildings['geometry']
# %%
df_hk_roads = geopandas.read_file('data/roads_FSDT/CENTERLINE.json')
# %%
df_hk_slopes = geopandas.read_file('data/SMR_FSDT/SMR_BDY_POLY.json')
# df_hk_govland = geopandas.read_file('data/govland_FSDT/GovernmentLandAllocation.json')
# %%
df_bldg_pos = geopandas.sjoin(df_hk_buildings, df_openspace, how = 'inner')
# %%
df_hk_buildings['CATEGORY']
plot_bldg_pos = df_bldg_pos.plot(figsize = (12,12),
                                   cmap = 'RdYlBu',
                                   column = 'CATEGORY',
                                   legend = True)
plot_bldg_pos = df_hk_roads.plot(edgecolor = 'gray', linewidth = 0.75, 
                                 ax = plot_bldg_pos)
plot_bldg_pos.set_ylim([815000, 822500])
plot_bldg_pos.set_xlim([832500, 837500])


# %%
df_bldg_pos = df_bldg_pos.drop(columns = ['STATUSDATE', 'LASTUPDATE'])
# join_bldg_pos.explore().save('map.html')

#%%
df_bldg_slopes = geopandas.sjoin(df_hk_buildings, df_hk_slopes, how = 'inner')
plot_bldg_slopes = df_bldg_slopes.plot(figsize = (12,12),
                                   cmap = 'RdYlBu',
                                   column = 'CATEGORY',
                                   legend = True)
plot_bldg_slopes = df_hk_roads.plot(edgecolor = 'gray', linewidth = 0.75,
                                    ax = plot_bldg_slopes)
plot_bldg_slopes.set_xlim([830000,845000])
plot_bldg_slopes.set_ylim([810000,825000])

#%%
df_map = geopandas.read_file('data/map_topographic_50000/ELEVLINE.json')
plot_map = df_map.plot()
plot_map.set_xlim([830000,845000])
plot_map.set_ylim([810000,825000])



#%%
df_bldg_slopes_json = df_bldg_slopes.to_json()

app = Dash()

app.layout = dash_leaflet.Map(
    [dash_leaflet.TileLayer(),
     dash_leaflet.GeoJSON(data=df_bldg_slopes_json,
                          zoomToBounds=True, zoomToBoundsOnClick=True)    
     ],
    style = {'width': '10-0px', 'height': '500px'}
    )



#%%
if __name__ == '__main__':
    app.run_server()




















