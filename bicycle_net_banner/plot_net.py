import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
# from matplotlib.collections import PatchCollection

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


def flatten(list):
    return([item for sublist in list for item in sublist])


#%%
df['lons'] = df.SHAPE.apply(rm_linestring, idx=0)
df['lats'] = df.SHAPE.apply(rm_linestring, idx=1)

df = df[['M18_RANG_SUB', 'RANG', 'lons', 'lats']]

#%%


# Nebennetz + Hauptnetz
df_select = df[df.RANG != 'H']
lons = flatten(df_select.lons)
lats = flatten(df_select.lats)

fig, ax = plt.subplots(figsize=(24, 10))
plt.plot(lons, lats, lw=0.5, color='gray')

df_select = df[df.RANG == 'H']
lons = flatten(df_select.lons)
lats = flatten(df_select.lats)

plt.plot(lons, lats, lw=1, color='gray')

xlim = (plt.xlim())
ylim = (plt.ylim())
plt.axis('off')
plt.savefig('banner_NH.svg')
plt.savefig('banner_NH.pdf')
plt.savefig('banner_NH.jpeg', dpi=350)


#%%

# only Hauptnetz
df_select = df[df.RANG == 'H']
lons = flatten(df_select.lons)
lats = flatten(df_select.lats)

fig, ax = plt.subplots(figsize=(24, 10))
plt.plot(lons, lats, lw=1, color='gray')
plt.axis('off')
plt.xlim(xlim)
plt.ylim(ylim)
plt.savefig('banner_H.svg')
plt.savefig('banner_H.pdf')
plt.savefig('banner_H.jpeg', dpi=350)

#%%


df_realnut = pd.read_csv('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:REALNUT2018OGD%20&srsName=EPSG:4326&outputFormat=csv')

#%%


def rm_polygon(x):
    if x[:7] == 'POLYGON':
        coords = [list(map(float, linestring.split(' '))) for linestring in x[10:-2].split(', ')] + [[0, 0]]
        return(coords)
    if x[:12] == 'MULTIPOLYGON':
        coords = []
        for linestrings in x[16:-3].split('), ('):
            coords += [list(map(float, linestring.split(' '))) for linestring in linestrings.split(', ')] + [[0, 0]]
        return(coords)
    else:
        print(x[:7])


#%%

df_realnut['polygon_edges'] = df_realnut.SHAPE.apply(rm_polygon)
df_realnut = df_realnut[['polygon_edges', 'NUTZUNG_LEVEL2']]

#%%

fig, ax = plt.subplots(figsize=(24, 10))
patches = []

cats = ['Naturraum', 'Landwirtschaft', 'Gewässer', 'Erholungs- u. Freizeiteinrichtungen']
colors = ['#058061', '#3db769', '#6dc9c8', '#3cba8e']
alphas = [0.5, 0.5, 0.3, 0.5]
for l2, color, alpha in zip(cats, colors, alphas):
    df_realnut_select = df_realnut[df_realnut.NUTZUNG_LEVEL2 == l2]
    polygon_edges = np.asarray(flatten(df_realnut_select.polygon_edges))
    polygon = Polygon(polygon_edges, facecolor=color, lw=0, alpha=alpha)
    patches.append(polygon)
    ax.add_artist(polygon)

# p = PatchCollection(patches, alpha=0.6, match_original=True)
# ax.add_collection(p)

df_select = df[df.RANG == 'H']
lons = flatten(df_select.lons)
lats = flatten(df_select.lats)
plt.plot(lons, lats, lw=1, color='gray')
plt.axis('off')

plt.xlim(xlim)
plt.ylim(ylim)

plt.savefig('banner_green.svg')
plt.savefig('banner_green.pdf')
plt.savefig('banner_green.jpeg', dpi=350)
plt.show()
