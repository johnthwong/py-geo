#%%
# ENVIRONMENT SETUP ----

import geopandas
from dash import Dash, dcc, html
import dash
import plotly.graph_objects as go
import plotly.express as px

# os.chdir("C:/Users/John TH Wong/Documents/py-geo")
# os.chdir("/Users/john/Library/Mobile Documents/com~Apple~CloudDocs/research/coding/py-geo")


# %%

#%%
df_bldg_slopes_0 = geopandas.read_file('df_bldg_slopes.geojson') 

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

districts = df_bldg_slopes_0['district'].sort_values().unique()
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
        _df = df_bldg_slopes_0
        # _lat = 22.3193
        # _lon = 114.1694
    else:
        _df = df_bldg_slopes_0.query(
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



