import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# constants
map_data = './data/wilm_to_buf_gps.csv'
run_data = './data/run_data.csv'
api_token = open('./cfg/api_key.txt', 'r').read()
mapbox_style = 'mapbox://styles/thepinkfreudian/ckxy1j35q179814ql82sa5sct'
site_css = { 'colors': {'darkgrey': '#141414', 'lightgrey': '#555555', 'pink': '#E12194', 'cyan': '#43C3CF', 'white': '#FFFFFF'},
             'fonts': {'headings': 'Roboto, Droid Sans', 'paragraph': 'Lora, Droid Serif'}
             }

# functions
def get_route_milestones(map_df):

    milestones = {
        'latitudes': [map_df['lat'][0], map_df['lat'][len(map_df)/2], map_df['lat'][len(map_df)-1]],
        'longitudes': [map_df['lon'][0], map_df['lon'][len(map_df)/2], map_df['lon'][len(map_df)-1]],
        'labels': ['START - Wilmington, NC', 'MIDPOINT', 'END - Buffalo, NY']
        }

    return milestones


# define layout css
base_font = dict(size=16, family=site_css['fonts']['headings'], color=site_css['colors']['cyan'])
annotation_font = dict(color=site_css['colors']['pink'], size=24, family=site_css['fonts']['headings'])

base_layout = dict(
    font = base_font,
    autosize = True,
    margin = dict(b=0, l=0, r=0, t=0),
    mapbox_accesstoken = api_token,
    mapbox_style = mapbox_style,
    showlegend = False
    )    

# get data frames from CSVs
map_df = pd.read_csv(map_data)
run_df = pd.read_csv(run_data)


# calculate route milestones and points of interest for map markers
milestones = get_route_milestones(map_df)
poi = {
    'latitudes': [36.5641, 38.78128, 39.59517, 39.71563, 41.99633],
    'longitudes': [-78.54295, -78.89605, -78.77808, -78.72772, -78.61579],
    'labels': ['NC/VA Border', 'VA/WVA Border', 'WVA/MD Border', 'MD/PA Border', 'PA/NY Border']
    }


# calculate miles run and generate data frame of only reached coordinates
total_miles = round(sum(run_df['miles']), 2)
coordinates_run = map_df[map_df['cumulative_distance_mi'] <= total_miles]


# generate base tile map zoomed to route and set layout properties
fig = px.scatter_mapbox(
    data_frame = map_df,
    lat = 'lat',
    lon = 'lon',
    size_max = 50,
    zoom = 5,
    color_discrete_sequence = [site_css['colors']['lightgrey']]
    )

fig.update_layout(base_layout)


# add trace for coordinates run
fig.add_scattermapbox(
    below = False,
    lat = coordinates_run['lat'],
    lon = coordinates_run['lon'],
    marker = dict(size=6, color=site_css['colors']['pink']),
    )


# add trace for route milestones
fig.add_scattermapbox(
    lat = milestones['latitudes'],
    lon = milestones['longitudes'],
    mode = 'markers+text',
    text = milestones['labels'],
    textfont = dict(color=site_css['colors']['cyan'], size=14),
    textposition = 'top right',
    marker_size=12,
    marker_color=site_css['colors']['cyan']
    )


# add trace for points of interest
fig.add_scattermapbox(
    lat = poi['latitudes'],
    lon = poi['longitudes'],
    mode = 'markers+text',
    text = poi['labels'],
    textfont = dict(color=site_css['colors']['white'], size=12),
    textposition = 'top right',
    marker_size = 12,
    marker_color = site_css['colors']['white']
)

# add miles run : total miles annotation
fig.add_annotation(
    font = annotation_font,
    bgcolor = site_css['colors']['darkgrey'],
    x = 0.05,
    y = .9,
    showarrow = False,
    text = 'Total miles completed: ' + str(total_miles) + ' of 711',
    textangle = 0,
    xanchor = 'left',
    xref = 'paper',
    yref = 'paper'
    )

# display final map
fig.show()
