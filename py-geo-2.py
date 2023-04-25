#%%
# ENVIRONMENT SETUP ----

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import geopandas
# import shapely
# import pysal 
#  the pysal metapackage doesnt actually contain any code, just a set of dependencies on its constituent subpackages. 
# Chances are good you don't actually need everything in the metapackage, 
# so you could also install the subpackages you are looking to use directly
# import fiona
# import pyproj
import pyrosm
# import osmnx
import matplotlib
import os
# pip install folium matplotlib mapclassify

os.getcwd()
# os.chdir("C:/Users/John TH Wong/Documents")
# os.chdir("/Users/john/Library/Mobile Documents/com~Apple~CloudDocs/research/coding/py-geo")
wd = print(os.getcwd())


# %% 
# CSDI PORTAL DATA ----

fp_a = "data/POS.json" # Public Open Space
df_a = geopandas.read_file(fp_a)

fp_b = "data/DCD.json" # District Council Boundaries

df_b = geopandas.read_file(fp_b)

# %%
df_a.head()
df_b.head()
#%%
df_a = df_a.drop(columns = 'LASTUPDATE')
df_a.explore()
df_b.explore()

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
# this merges buildings to observations of restautrants, where the two intersect
# the predicate argument, unused below, defaults to intersects; others include contains, crosses, etc.
# .sjoin_nearest() joins based on "closest", with max distance set by user, rather than "touching"
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
# overlay = geopandas.overlay(restaurants, buildings, how = 'intersection', keep_geom_type = False)

# %%
roads = osm.get_network()
# %%
plot = join.plot(column = 'building_left', figsize = (12,12), cmap = 'RdYlBu', legend = True)
plot = roads.plot(edgecolor = 'gray', linewidth = 0.75,
                ax = plot # this argument aligns the roads.plot with the plot object from previous line
                )
plot.set_ylim([52.36, 52.38])
plot.set_xlim([4.88, 4.91])


# %%
# CSDI PORTAL DATA 2 ----

hk_buildings = geopandas.read_file('data/building_FSDT/BUILDING_STRUCTURE.json')
# %%
hk_buildings.plot()
# hk_buildings.explore().save('map.html')
# %%
# hk_buildings.describe()
hk_buildings.columns
hk_buildings['geometry']
# %%
hk_roads = geopandas.read_file('data/roads_FSDT/CENTERLINE.json')
# %%
# hk_buildings.explore()
# %%
# hk_slopes = geopandas.read_file('data/SMR_FSDT/SMR_BDY_POLY.json')
# hk_govland = geopandas.read_file('data/govland_FSDT/GovernmentLandAllocation.json')
# %%
join_bldg_pos = geopandas.sjoin(hk_buildings, df_a, how = 'inner')
# %%
hk_buildings['CATEGORY']
plot_bldg_pos = join_bldg_pos.plot(figsize = (12,12),
                                   cmap = 'RdYlBu',
                                   column = 'CATEGORY',
                                   legend = True)
plot_bldg_pos = hk_roads.plot(edgecolor = 'gray', linewidth = 0.75, ax = plot_bldg_pos)
plot_bldg_pos.set_ylim([815000, 822500])
plot_bldg_pos.set_xlim([832500, 837500])


# %%
join_bldg_pos = join_bldg_pos.drop(columns = ['STATUSDATE', 'LASTUPDATE'])
join_bldg_pos.explore().save('map.html')


