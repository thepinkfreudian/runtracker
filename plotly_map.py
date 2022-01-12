import pandas as pd
import plotly.express as px
import MySQLdb as sql
import chart_studio.plotly as py

import utils.utils as utils
import utils.database as db
from setup import push, config, environment
from api_data import api_data

# function definitions
def get_data(cursor, table):

    columns, data = utils.select_all(cursor, table)
    df = pd.DataFrame(data, columns=columns)

    return df


def get_route_milestones(map_df, start_point, end_point):

    milestones = {
        'latitude': [map_df['latitude'][0], map_df['latitude'][int(round(len(map_df)/2))], map_df['latitude'][len(map_df)-1]],
        'longitude': [map_df['longitude'][0], map_df['longitude'][int(round(len(map_df)/2))], map_df['longitude'][len(map_df)-1]],
        'label': ['START - ' + start_point, 'MIDPOINT', 'END - ' + end_point]
        }

    return milestones


api_key = config['api_key']
mapbox_style = config['mapbox_style']
dashboard_name = config['dashboard_name']
start_point = config['start_point']
end_point = config['end_point']
sql_config = config['sql_config']
site_css = config['site_css']
insert_table = config['insert_tables'][environment]
table_list = config['table_list']


# connect to mySQL instance
conn = sql.connect(sql_config['hostname'],
                   sql_config['username'],
                   sql_config['password'],
                   sql_config['db'])
cursor = conn.cursor()

# update database with Google fit data
db.update_database(conn, api_data, insert_table)

# bring mySQL data into DataFrames
dfs = []
for table in table_list:
    df = get_data(cursor, table)
    dfs.append(df)

map_df = dfs[0]
run_df = dfs[1]
poi_df = dfs[2]


# calculate route milestones and points of interest for map markers
milestones = get_route_milestones(map_df, start_point, end_point)


# calculate miles run and generate data frame of only reached coordinates
total_miles = round(sum(run_df['miles']), 2)
coordinates_run = map_df[map_df['cumulative_distance_mi'] <= total_miles]


# define layout css
base_font = dict(size=16, family=site_css['fonts']['headings'], color=site_css['colors']['cyan'])
annotation_font = dict(color=site_css['colors']['pink'], size=24, family=site_css['fonts']['headings'])

base_map_config = dict(data_frame=map_df,
                   lat='latitude',
                   lon='longitude',
                   size_max=50,
                   zoom=5,
                   color_discrete_sequence=[site_css['colors']['lightgrey']])

base_layout = dict(font=base_font,
               autosize=True,
               margin=dict(b=0, l=0, r=0, t=0),
               mapbox_accesstoken=api_key,
               mapbox_style=mapbox_style,
               showlegend=False
               )

coordinates_run_config = dict(lat=coordinates_run['latitude'],
                          lon=coordinates_run['longitude'],
                          marker=dict(size=6, color=site_css['colors']['pink'])
                          )

milestones_config = dict(lat=milestones['latitude'],
                     lon = milestones['longitude'],
                     mode='markers+text',
                     text=milestones['label'],
                     textfont=dict(color=site_css['colors']['cyan'], size=14),
                     textposition='top right',
                     marker_size=12,
                     marker_color=site_css['colors']['cyan']
                    )

poi_config = dict(lat = poi_df['latitude'],
              lon = poi_df['longitude'],
              mode = 'markers+text',
              text = poi_df['label'],
              textfont = dict(color=site_css['colors']['white'], size=12),
              textposition = 'top right',
              marker_size = 12,
              marker_color = site_css['colors']['white']
              )

annotation_layout = dict(font = annotation_font,
                     bgcolor = site_css['colors']['darkgrey'],
                     x = 0.05,
                     y = .9,
                     showarrow = False,
                     text = 'Total miles completed: ' + str(total_miles) + ' of 711',
                     textangle = 0,
                     xanchor = 'left',
                     xref = 'paper',
                     yref = 'paper')


# generate base tile map zoomed to route and set layout properties
fig = px.scatter_mapbox(**base_map_config)
fig.update_layout(base_layout)

# add trace for coordinates run
fig.add_scattermapbox(**coordinates_run_config)

# add trace for route milestones
fig.add_scattermapbox(**milestones_config)

# add trace for points of interest
fig.add_scattermapbox(**poi_config)

# add miles run : total miles annotation
fig.add_annotation(**annotation_layout)


# push to plotly or show map locally depending on value of 'push'
if push:
    py.plot(fig, filename = dashboard_name, auto_open=True)
else:
    # display final map
    fig.show()

