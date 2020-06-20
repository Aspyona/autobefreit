import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
import matplotlib.pyplot as plt
import os
import numpy as np

df = pd.read_csv('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:RADNETZOGD%20&srsName=EPSG:4326&outputFormat=csv')


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


flatten = lambda l: [item for sublist in l for item in sublist]


#%%
df['lons'] = df.SHAPE.apply(rm_linestring, idx=0)
df['lats'] = df.SHAPE.apply(rm_linestring, idx=1)

df = df[['M18_RANG_SUB', 'RANG', 'lons', 'lats']]

#%%

df_select = df[df.RANG == 'H']
df_select = df
lons = flatten(df_select.lons.values)
lats = flatten(df_select.lats.values)

#%%

fix, ax = plt.subplots(figsize=(24, 10))
plt.plot(lons, lats, lw=1, color='black')
plt.axis('off')
plt.savefig('banner.svg')
plt.savefig('banner.pdf')
#%%
