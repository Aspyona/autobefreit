import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

df = pd.read_csv('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:RADNETZOGD%20&srsName=EPSG:4326&outputFormat=csv')

# 2018
# df_realnut = pd.read_csv('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:REALNUT2018OGD%20&srsName=EPSG:4326&outputFormat=csv')

# 2020
df_realnut = pd.read_csv(
    'https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=csv&typeName=ogdwien:REALNUT2020OGD')


# %%


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


def rm_polygon_str(x):
    if x[:7] == 'POLYGON':
        coords = ' M ' + ' L'.join([','.join(linestring.split(' ')) for linestring in x[10:-2].split(', ')])
        return(coords)
    if x[:12] == 'MULTIPOLYGON':
        coords = ''
        for linestrings in x[16:-3].split('), ('):
            coords += ' M ' + ' L'.join([','.join(linestring.split(' ')) for linestring in linestrings.split(', ')])
        return(coords)
    else:
        print(x[:7])


def rm_polygon(x):
    if x[:7] == 'POLYGON':
        coords = [list(map(float, linestring.split(' '))) for linestring in x[10:-2].split(', ')] + [[0, 0]]
        return(coords)
    if x[:12] == 'MULTIPOLYGON':
        coords = []
        for linestrings in x[16:-3].split('), ('):
            if linestrings[-1] == ')':
                linestrings = linestrings[:-1]
            if linestrings[0] == '(':
                linestrings = linestrings[1:]
            coords += [list(map(float, linestring.split(' '))) for linestring in linestrings.split(', ')] + [[0, 0]]
        return(coords)
    else:
        print(x[:7])


# %%

df_realnut['polygon_edges'] = df_realnut.SHAPE.apply(rm_polygon_str)
df_realnut['polygon_edges_for_matplotlib'] = df_realnut.SHAPE.apply(rm_polygon)
# df_realnut = df_realnut[['polygon_edges', 'NUTZUNG_LEVEL2']]

# %%

df['lons'] = df.SHAPE.apply(rm_linestring, idx=0)
df['lats'] = df.SHAPE.apply(rm_linestring, idx=1)

df = df[['M18_RANG_SUB', 'RANG', 'lons', 'lats']]

# %%

df_realnut.loc[df_realnut.NUTZUNG_LEVEL2 == 'weitere verkehrliche Nutzungen',
               'NUTZUNG_LEVEL2'] = df_realnut.loc[df_realnut.NUTZUNG_LEVEL2 == 'weitere verkehrliche Nutzungen', 'NUTZUNG_LEVEL3']
df_realnut.loc[df_realnut.NUTZUNG_LEVEL2 == 'Straßenraum', 'NUTZUNG_LEVEL2'] = 'Straßenraum u. Parkplätze'
df_realnut.loc[df_realnut.NUTZUNG_LEVEL2 == 'Parkplätze u. Parkhäuser', 'NUTZUNG_LEVEL2'] = 'Straßenraum u. Parkplätze'

# %%

use_color = True

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
plt.show()

fig, ax = plt.subplots(figsize=(24, 10))
patches = []

cats = [
    # 'weitere verkehrliche Nutzungen',
    'Straßenraum u. Parkplätze', 'Wohn- u. Mischnutzung (Schwerpunkt Wohnen)', 'Naturraum',
    'Landwirtschaft', 'Industrie- und Gewerbenutzung', 'Gewässer',
    'Geschäfts,- Kern- und Mischnutzung (Schwerpunkt betriebl. Tätigkeit)',
    'Erholungs- u. Freizeiteinrichtungen',
    'Technische Infrastruktur/Kunstbauten/Sondernutzung',
    'soziale Infrastruktur',
    'Transport und Logistik inkl. Lager',
    'Bahnhöfe und Bahnanlagen',
    'Sonstiges',
]

label_colors = {'Wohn- u. Mischnutzung (Schwerpunkt Wohnen)': '#EF553B',
                'Naturraum': '#FECB52',
                'Landwirtschaft': 'rgb(17, 119, 51)',
                'Transport und Logistik inkl. Lager': '#B6E880',
                'Industrie- und Gewerbenutzung': '#FF97FF',
                'Gewässer': '#19D3F3',
                'Geschäfts,- Kern- und Mischnutzung (Schwerpunkt betriebl. Tätigkeit)': '#00CC96',
                'Erholungs- u. Freizeiteinrichtungen': '#FFA15A',
                'Technische Infrastruktur/Kunstbauten/Sondernutzung': 'rgb(153, 153, 51)',
                'soziale Infrastruktur': '#AB63FA',
                'Bahnhöfe und Bahnanlagen': '#FF6692',
                'Sonstiges': 'rgb(51, 34, 136)',
                # 'Straßenraum': '#636EFA',
                'Straßenraum u. Parkplätze': '#636EFA',
                # 'weitere verkehrliche Nutzungen': '#636EFA',
                }


def rgb_to_hex(r, g, b):
    return ('#{:X}{:X}{:X}').format(r, g, b)


colors = ['white', 'gray']
colors += ['white'] * 10

for l2, color in zip(cats, colors):

    if use_color:
        color = label_colors[l2]
        if color[:3] == 'rgb':
            color = color[4:-1]
            color = color.split(', ')
            color = rgb_to_hex(int(color[0]), int(color[1]), int(color[2]))

    df_realnut_select = df_realnut[df_realnut.NUTZUNG_LEVEL2 == l2]
    polygon_edges = np.asarray(flatten(df_realnut_select.polygon_edges_for_matplotlib))
    polygon = Polygon(polygon_edges, facecolor=color, lw=0)
    patches.append(polygon)
    ax.add_artist(polygon)

p = PatchCollection(patches, alpha=0.7, match_original=True)
ax.add_collection(p)

plt.axis('off')
plt.xlim(xlim)
plt.ylim(ylim)

if use_color:
    plt.savefig('realnut_map.pdf')
    plt.savefig('realnut_map.jpeg', dpi=450)
else:
    plt.savefig('banner_street.svg')
    plt.savefig('banner_street.pdf')
    plt.savefig('banner_street.jpeg', dpi=350)

plt.show()

# %%


# bugs with Straßenraum? Plot first, so other categories are on top
# hovertext not possible with shapes

colors = [c for c in px.colors.qualitative.Plotly]
colors += ['PaleTurquoise']

fig = go.Figure()

df_realnut.NUTZUNG_LEVEL2.unique()

# cats = ['Straßenraum', 'Wohn- u. Mischnutzung (Schwerpunkt Wohnen)', 'Naturraum',
#         'Landwirtschaft', 'weitere verkehrliche Nutzungen',
#         'Gewässer', 'Industrie- und Gewerbenutzung',
#         'Geschäfts,- Kern- und Mischnutzung (Schwerpunkt betriebl. Tätigkeit)',
#         'Erholungs- u. Freizeiteinrichtungen',
#         'Technische Infrastruktur/Kunstbauten/Sondernutzung',
#         'soziale Infrastruktur']

shapes = []
for cat, color in zip(cats, colors):
    print(cat)
    df_realnut_select = df_realnut[df_realnut.NUTZUNG_LEVEL2 == cat]
    polygon_edges = ''.join(df_realnut_select.polygon_edges)
    shapes.append(dict(type="path", path=polygon_edges, fillcolor=color, line=dict(width=0), ))  # line_color="LightSeaGreen",

    fig.add_trace(go.Scatter(
        name=cat,
        x=[0],
        y=[0],
        opacity=1,
        text=cat,
        mode='markers',
        showlegend=True,
        marker=dict(
            color=color,
        ),
        hoverinfo='skip',
    )
    )

fig.update_layout(
    shapes=shapes,
    xaxis={
        'range': xlim,
        'showgrid': False,  # thin lines in the background
        'zeroline': False,  # thick line at x=0
        'visible': False,  # numbers below
    },
    yaxis={
        'range': ylim,
        'showgrid': False,  # thin lines in the background
        'zeroline': False,  # thick line at x=0
        'visible': False,  # numbers below
    },
    hovermode='x',
)

fig.update_layout(legend=dict(x=1, y=1, traceorder="normal", xanchor='left', itemclick=False, itemdoubleclick=False))
fig.update_layout(autosize=True)
pio.write_html(fig, file='html/index2.html', auto_open=False, include_plotlyjs="cdn")  # , include_mathjax="cdn")

fig.show()

# %%
# %%
# %%
