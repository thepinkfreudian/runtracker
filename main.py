import sys
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import MySQLdb as sql

# set variable at commandline to push changes to plotly host when script is run
push = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'push':
        push = True
    else:
        argv = str(sys.argv[1])
        print('Invalid value \'' + argv + '\' passed as sys.argv[1].')
        sys.exit(1)


# constants
config_file = './cfg/config.json'


# functions
def get_session_config(config_file):

    with open(config_file, 'r') as f:
        config = json.load(f)

    return config

def get_sql_data(cursor, table):

    cols_query = 'SHOW COLUMNS FROM ' + table
    data_query = 'SELECT * FROM ' + table

    cursor.execute(cols_query)
    cols = cursor.fetchall()
    columns = [col[0] for col in cols]

    cursor.execute(data_query)
    data = cursor.fetchall()
    
    df = pd.DataFrame(data, columns=columns)

    return df

def get_route_milestones(map_df):

    milestones = {
        'latitude': [map_df['latitude'][0], map_df['latitude'][int(round(len(map_df)/2))], map_df['latitude'][len(map_df)-1]],
        'longitude': [map_df['longitude'][0], map_df['longitude'][int(round(len(map_df)/2))], map_df['longitude'][len(map_df)-1]],
        'label': ['START - Wilmington, NC', 'MIDPOINT', 'END - Buffalo, NY']
        }

    return milestones

# get config
config = get_session_config(config_file)

api_key = config['api_key']
mapbox_style = config['mapbox_style']
dashboard_name = config['dashboard_name']
sql_config = config['sql_config']
site_css = config['site_css']
table_list = config['table_list']

# define layout css
base_font = dict(size=16, family=site_css['fonts']['headings'], color=site_css['colors']['cyan'])
annotation_font = dict(color=site_css['colors']['pink'], size=24, family=site_css['fonts']['headings'])

base_layout = dict(
    font = base_font,
    autosize = True,
    margin = dict(b=0, l=0, r=0, t=0),
    mapbox_accesstoken = api_key,
    mapbox_style = mapbox_style,
    showlegend = False
    )    

# connect to mySQL instance
conn = sql.connect(sql_config['hostname'],
                   sql_config['username'],
                   sql_config['password'],
                   sql_config['db'])
cursor = conn.cursor()

# bring mySQL data into DataFrames
dfs = []
for table in table_list:
    df = get_sql_data(cursor, table)
    dfs.append(df)
    
map_df = dfs[0]
run_df = dfs[1]
poi_df = dfs[2]

# calculate route milestones and points of interest for map markers
milestones = get_route_milestones(map_df)


# calculate miles run and generate data frame of only reached coordinates
total_miles = round(sum(run_df['miles']), 2)
coordinates_run = map_df[map_df['cumulative_distance_mi'] <= total_miles]


# generate base tile map zoomed to route and set layout properties
fig = px.scatter_mapbox(
    data_frame = map_df,
    lat = 'latitude',
    lon = 'longitude',
    size_max = 50,
    zoom = 5,
    color_discrete_sequence = [site_css['colors']['lightgrey']]
    )

fig.update_layout(base_layout)


# add trace for coordinates run
fig.add_scattermapbox(
    below = False,
    lat = coordinates_run['latitude'],
    lon = coordinates_run['longitude'],
    marker = dict(size=6, color=site_css['colors']['pink']),
    )


# add trace for route milestones
fig.add_scattermapbox(
    lat = milestones['latitude'],
    lon = milestones['longitude'],
    mode = 'markers+text',
    text = milestones['label'],
    textfont = dict(color=site_css['colors']['cyan'], size=14),
    textposition = 'top right',
    marker_size=12,
    marker_color=site_css['colors']['cyan']
    )


# add trace for points of interest
fig.add_scattermapbox(
    lat = poi_df['latitude'],
    lon = poi_df['longitude'],
    mode = 'markers+text',
    text = poi_df['label'],
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


# push to plotly or show map locally depending on value of 'push'
import chart_studio.plotly as py

if push:
    py.plot(fig, filename = dashboard_name, auto_open=True)
else:
    # display final map
    fig.show()
