#%%
# ENVIRONMENT SETUP ----

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import geopandas
import shapely
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
import dash
import dash_leaflet
import plotly.graph_objects as go
import plotly.express as px
import json
import pandas


os.getcwd()
# os.chdir("C:/Users/John TH Wong/Documents/py-geo")
# os.chdir("/Users/john/Library/Mobile Documents/com~Apple~CloudDocs/research/coding/py-geo")
def wd(): 
    return os.getcwd()
wd = wd()

# %% 
# CSDI PORTAL DATA ----

# =============================================================================
# df_hk_openspace = geopandas.read_file("data/POS.json") # Public Open Space
# 
# # %%
# df_hk_openspace.head()
# #%%
# df_hk_openspace = df_hk_openspace.drop(columns = 'LASTUPDATE')
# df_hk_openspace.explore()
# =============================================================================

# %%
# =============================================================================
# # OPENSTREETMAP DATA ----
# 
# fp = pyrosm.get_data("test_pbf")
# 
# # %%
# fp_1 = pyrosm.get_data("Amsterdam")
# #%%
# osm = pyrosm.OSM(fp_1)
# # %%
# buildings = osm.get_buildings()
# # buildings.plot()
# # len(buildings)
# # buildings.explore()
# #%%
# buildings.plot()
# 
# # %%
# # pyrosm.data.sources.available.keys()
# pyrosm.data.sources.cities.available
# pyrosm.data.sources.subregions.available.keys()
# pyrosm.data.sources.asia.available
# 
# #%%
# help(pyrosm.OSM)
# 
# # %%
# buildings.crs
# buildings_3067 = buildings.to_crs(epsg = 3067)
# buildings_3067.plot()
# 
# # extracts the geometry of the first-indexed in the buildings object 
# geom = buildings.loc[0, "geometry"]
# geom_3067 = buildings_3067.loc[0, "geometry"]
# # geom
# geom_3067
# type(geom_3067)
# type(buildings)
# 
# # %%
# buildings_3067.area
# buildings_3067.area.describe()
# 
# # %%
# # osm is an object defined earlier.
# # get_pois stands for get points of interests
# restaurants = osm.get_pois(custom_filter = {'amenity': ['restaurant']} )
# 
# # %%
# restaurants.plot()
# 
# # %%
# # this merges buildings to observations of restautrants, 
#     # where the two intersect
# # the predicate argument, unused below, defaults to intersects; 
#     # others include contains, crosses, etc.
# # .sjoin_nearest() joins based on "closest", 
#     # with max distance set by user, rather than "touching"
# # overlay() keeps both rather than merges
# # .sjoin can be called from both geopandas package and GeoDataFrames objects
# join = geopandas.sjoin(buildings, restaurants, how = 'inner')
# 
# # %%
# join.plot()
# # %% 
# buildings.describe()
# buildings
# buildings.columns
# type(buildings['geometry'])
# # overlay = geopandas.overlay(restaurants, buildings, 
# #                             how = 'intersection', keep_geom_type = False)
# 
# # %%
# roads = osm.get_network()
# # %%
# plot = join.plot(column = 'building_left', figsize = (12,12), cmap = 'RdYlBu', 
#                  legend = True)
# plot = roads.plot(edgecolor = 'gray', linewidth = 0.75,
#                  # this argument aligns the roads.plot with the plot object 
#                      # from previous line
#                 ax = plot 
#                 )
# plot.set_ylim([52.36, 52.38])
# plot.set_xlim([4.88, 4.91]) 
# 
# =============================================================================


# %%
# CSDI PORTAL DATA 2 ----

df_hk_buildings = geopandas.read_file('data/building_FSDT/BUILDING_STRUCTURE.json')
df_hk_bldg_cat = geopandas.read_file('data/building_FSDT/CT_BUILDING_CATEGORY.json')
df_hk_roads = geopandas.read_file('data/roads_FSDT/CENTERLINE.json')
df_hk_slopes = geopandas.read_file('data/SMR_FSDT/SMR_BDY_POLY.json')
df_hk_map = geopandas.read_file('data/map_topographic_50000/ELEVPOLY.json')
df_hk_dist_boundaries = (geopandas.read_file("data/DCD.json") # District Council Boundaries
                         .to_crs(epsg = 4326)
                         .assign(center = lambda df_hk_dist_boundaries: df_hk_dist_boundaries.centroid)
                         )
# df_hk_govland = geopandas.read_file('data/govland_FSDT/GovernmentLandAllocation.json')

# df_bldg_pos = geopandas.sjoin(df_hk_buildings, df_hk_openspace, how = 'inner')
df_bldg_slopes = (geopandas.sjoin(df_hk_buildings, df_hk_slopes, how = 'inner')
                  .rename(columns = {
                      'OBJECTID_left' : 'id_bldg',
                      'SHAPE_Length_left' : 'shape_length_bldg',
                      'SHAPE_Area_left' : 'shape_area_bldg',
                      'index_right': 'index_slope',
                      'OBJECTID_right': 'id_slope',
                      'SHAPE_Length_right': 'shape_length_slope',
                      'SHAPE_Area_right': 'shape_area_slope'
                      })
                  .to_crs(epsg = 4326)
                  )

df_hk_bldg_cat = df_hk_bldg_cat.rename(columns = {'CODE': 'CATEGORY',
                                                  'DESCRIPTION': 'CATEGORY_DESC'})
df_bldg_slopes['CATEGORY'] = df_bldg_slopes['CATEGORY'].astype(int)

df_bldg_slopes_0 = pandas.merge(df_bldg_slopes, df_hk_bldg_cat[['CATEGORY', 'CATEGORY_DESC']], 
                                on = 'CATEGORY', how = 'left')

df_bldg_slopes_1 = (geopandas.sjoin(df_bldg_slopes_0, 
                                   df_hk_dist_boundaries[['NAME_EN', 'geometry', 'center']], 
                                   how = 'left', predicate = 'within')
                    .rename(columns={'NAME_EN': 'district'})
                    )


# %%
df_hk_buildings.plot()
# %%
# df_hk_buildings.describe()
df_hk_buildings.columns
# df_hk_buildings['geometry']
#%%
plot_map = df_hk_map.plot()
plot_map.set_xlim([830000,845000])
plot_map.set_ylim([810000,825000])


# %%
# =============================================================================
# df_hk_buildings['CATEGORY']
# plot_bldg_pos = df_bldg_pos.plot(figsize = (12,12),
#                                    cmap = 'RdYlBu',
#                                    column = 'CATEGORY',
#                                    legend = True)
# plot_bldg_pos = df_hk_roads.plot(edgecolor = 'gray', linewidth = 0.75, 
#                                  ax = plot_bldg_pos)
# # plot_bldg_pos = df_hk_map.plot(color = 'gray', ax = plot_bldg_pos)
# plot_bldg_pos.set_ylim([815000, 822500])
# plot_bldg_pos.set_xlim([832500, 837500])
# 
# =============================================================================

# %%
# =============================================================================
# df_bldg_pos = df_bldg_pos.drop(columns = ['STATUSDATE', 'LASTUPDATE'])
# # join_bldg_pos.explore().save('map.html')
# =============================================================================


#%%
plot_bldg_slopes = df_hk_map.plot(color = 'whitesmoke',
                                  figsize = (12, 12))
plot_bldg_slopes = df_bldg_slopes.plot(figsize = (12,12),
                                   cmap = 'RdYlBu',
                                   column = 'CATEGORY',
                                   legend = True,
                                   ax = plot_bldg_slopes)
plot_bldg_slopes = df_hk_roads.plot(edgecolor = 'grey', linewidth = 0.75,
                                    ax = plot_bldg_slopes)
plot_bldg_slopes.set_xlim([830000,845000])
plot_bldg_slopes.set_ylim([810000,825000])





#%%
# df_bldg_slopes_json = df_bldg_slopes.to_json()

# app = Dash()

# app.layout = html.Div([
#     dash_leaflet.Map(children = [dash_leaflet.TileLayer(),
#                                  dash_leaflet.GeoJSON(id = 'districts',
#                                                       url='data/map_topographic_50000/BDRYLINE.json',
#                                                       zoomToBounds=True, zoomToBoundsOnClick=True
#                                                       )                         
#                                 ],
#     style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}
#     ),
#     html.Div(id = 'districts')
# ])

#%%
# =============================================================================
# fig = go.Figure(go.Scattergeo())
# fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()
# =============================================================================


#%%
# =============================================================================
# url = 'https://raw.githubusercontent.com/kefeimo/DataScienceBlog/master/2.geo_plot/df_mapbox_demo.csv'
# df_plot_tmp = pandas.read_csv(url)
# df_plot_tmp.head()
# # two-line code
# fig = px.scatter_mapbox(df_plot_tmp, lat="latitude", lon="longitude", color="gender", zoom=3, mapbox_style='open-street-map')
# fig.show()
# #%%
# lat = pandas.to_numeric(df_hk_openspace["LATITUDE"])
# lon = pandas.to_numeric(df_hk_openspace["LONGITUDE"])
# name = df_hk_openspace["NAME_EN"]
# color = df_hk_openspace["NSEARCH01_EN"]
# 
# fig = px.scatter_mapbox(lat=lat, lon=lon, zoom=10, mapbox_style='open-street-map',
#                         width = 1000, height = 1000, hover_name = name,
#                         color = color, size_max = 20)
# 
# fig.show()
# 
# =============================================================================
#%%
# json_1 = eval(df_bldg_slopes['geometry'].to_json())

# This one uses graph_objects mapbox
# =============================================================================
# fig = go.Figure(
#     go.Choroplethmapbox(
#         geojson=eval(df_bldg_slopes_1['geometry'].to_json()),
#         locations = df_bldg_slopes_1.index,
#         z = df_bldg_slopes_1['CATEGORY']
#     )
# )
# fig.update_layout(mapbox_style='open-street-map')
# =============================================================================

# This one uses plotly express mapbox
fig = px.choropleth_mapbox(
    geojson=eval(df_bldg_slopes_1['geometry'].to_json()),
    locations = df_bldg_slopes_1.index,
    color = df_bldg_slopes_1['CATEGORY'],
    mapbox_style='open-street-map',
    center = {"lat": 22.3193, "lon": 114.1694},
    zoom = 10
    )


# This one uses plotly express mapbox and the csdi-downloaded map
# =============================================================================
# df_hk_map_1 = df_hk_map.to_crs(epsg = 4326)
# df_hk_map_2 = eval(df_hk_map_1['geometry'].to_json())
# fig_1 = px.choropleth_mapbox(
#     geojson=eval(df_bldg_slopes_1['geometry'].to_json()),
#     locations = df_bldg_slopes_1.index,
#     color = df_bldg_slopes_1['CATEGORY'],
#     mapbox_style='white-bg',
#     center = {"lat": 22.3193, "lon": 114.1694},
#     zoom = 10
#     )
# 
# fig_1.update_layout(
#     mapbox_layers=[
#         {
#             "sourcetype": "geojson",
#             "sourceattribution": "CSDI",
#             "source": "https://mapapi.geodata.gov.hk/gs/api/v1.0.0/vt/basemap/WGS84/resources/styles/root.json"
# 
#         }
#     ]
# )
# =============================================================================


#%% Code from stackexchange for ref
# =============================================================================

# json_2 = eval(df_geo['geometry'].to_json())
# 
# df_geo = geopandas.read_file('https://raw.githubusercontent.com/kevalshah90/StroomWeb/23ef45e3d4da98ec0d6cae91842174411a403692/uscensusgeo.geojson')
# fig = go.Figure(
#     go.Choroplethmapbox(
#         geojson=eval(df_geo['geometry'].to_json()),  # note the 'eval' here
#         locations=df_geo.index,  # point to dataframe's index
#         z=df_geo['ALAND'],
#         colorscale="Viridis", 
#         zmin=df_geo['ALAND'].min(), 
#         zmax=df_geo['ALAND'].max(), 
#         marker_line_width=0
#     )
# )
# fig.update_layout(mapbox_style='open-street-map')
# fig.show()
# =============================================================================
#%%
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets = external_stylesheets)
# =============================================================================
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])
# =============================================================================

districts = df_bldg_slopes_1['district'].sort_values().unique()
def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

app.layout = html.Div([
    html.Div(className = 'header',
             children = [
                 html.H1(['Buildings Which Are in Close Proximity of Man-made Slopes'],
                     className = 'header-title'),
                html.P(
                    children = [
                        'Find out if a building is at risk during extreme weather'
                    ],
                    className = 'header-description')
                 ]),
    html.Div(
        className = 'menu',
        children = [
            html.Div(
                className = 'menu-wrapper',
                children = [
                    html.Div(className = 'menu-title'),
                    html.P('Select a district:'),
                    dcc.Dropdown(
                        className = 'dropdown',
                        id = 'district',
                        options = [{'label': district, 'value': district}
                                   for district in districts] #+ [{'label': 'Select all', 'value': 'all_districts'}]
                        ,
                        # value = 'all_districts',
                        value = 'Central and Western District',
                        clearable = False
                        ),
                ]
            )
        ]
    ),
    html.Div(
        className = 'wrapper',
        children=[
            html.Div(
                className = 'card',
                children = [dcc.Graph(id = 'fig_1',
                                      config = {'displayModeBar': False},
                                      figure = blank_figure()
                                      )]
            )
        ]
    )
    
])




@app.callback(
    dash.Output('fig_1', 'figure'),
    dash.Input('district', 'value')
    )
def display_map(district):
    if district == 'all_districts':
        _df = df_bldg_slopes_1
        # _lat = 22.3193
        # _lon = 114.1694
    else:
        _df = df_bldg_slopes_1.query(
            'district == @district')
        
        # _lat = (df_hk_dist_boundaries.query(
        #     'NAME_EN == @district')
        #     .center
        #     .x
        #     )
        # _lon = (df_hk_dist_boundaries.query(
        #     'NAME_EN == @district')
        #     .center
        #     .y
        #     )
    
    
    fig = px.choropleth_mapbox(
        geojson=eval(_df['geometry'].to_json()),
        locations = _df.index,
        color = _df['CATEGORY_DESC'],
        mapbox_style='open-street-map',
        # center = {"lat": _lat, "lon": _lon},
        center = {"lat": 22.3193, "lon": 114.1694},
        zoom = 12, height = 800
        )
    
    fig.update_layout( 
        legend=dict(
            title=None, orientation = 'h', y=1, yanchor="bottom", x=0.5, xanchor="center"
        )
    )
   
    return fig

#%%
if __name__ == '__main__':
    app.run_server()





















# %%
