import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
import os
import numpy as np

# pd.read_csv('https://www.wien.gv.at/gogv/l9ogdverkehrsflaechenbezirke2017', sep = ';')
df = pd.read_csv('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:RADNETZOGD%20&srsName=EPSG:4326&outputFormat=csv')


os.system('mkdir -p bicycle_map/existing')


#%%


def rm_linestring(x, idx):
    if x[:10] == 'LINESTRING':
        coords = [float(linestring.split(' ')[idx]) for linestring in x[12:-1].split(', ')] + [None]
        return(coords)
    if x[:15] == 'MULTILINESTRING':
        coords = []
        for linestrings in x[18:-2].split('), ('):
            coords += [float(linestring.split(' ')[idx]) for linestring in linestrings.split(', ')] + [None]
        return(coords)
    else:
        print(x)


def flatten(list):
    return([item for sublist in list for item in sublist])


#%%
df['lons'] = df.SHAPE.apply(rm_linestring, idx=0)
df['lats'] = df.SHAPE.apply(rm_linestring, idx=1)

df = df[['M18_RANG_SUB', 'lons', 'lats']]

#%%

fig = go.Figure()

for rang_sub, rang_sub_name, width in zip(['N', 'B', 'G', 'E'], ['Nebennetz', 'Basisroute', 'Grundnetz', 'erweitertes Grundnetz'], [3, 5, 5, 4]):
    df_select = df[df.M18_RANG_SUB == rang_sub]
    lons = flatten(df_select.lons)
    lats = flatten(df_select.lats)
    fig.add_trace(
        go.Scattermapbox(
            name=rang_sub_name,
            mode="lines", fill=None,
            lon=lons,
            lat=lats,
            line=dict(width=width),
            opacity=0.8,
            hoverinfo='name'
        )
    )

fig.update_layout(
    mapbox={'style': "stamen-terrain", 'center': {'lon': 16.363449, 'lat': 48.210033}, 'zoom': 11},
    showlegend=False,
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
)
# fig.update_layout(legend=dict(bordercolor='rgb(100,100,100)',
#                               borderwidth=2,
#                               itemclick='toggleothers',  # when you are clicking an item in legend all that are not in the same group are hidden
#                               x=0.91,
#                               y=1))
pio.write_html(fig, file='bicycle_map/existing/index.html', auto_open=False, include_plotlyjs="cdn")  # , include_mathjax="cdn")

del lons
del lats
#%%
