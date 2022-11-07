# street and bicycle map

import geopandas as gpd
import geoplot
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

# %%

wien = gpd.read_file(
    'https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:BEZIRKSGRENZEOGD&srsName=EPSG:4326&outputFormat=json')

# 2018
# df_realnut = gpd.read_file('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:REALNUT2018OGD%20&srsName=EPSG:4326&outputFormat=json')

# 2020
df_realnut = gpd.read_file(
    'https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:REALNUT2020OGD')


list(df_realnut)

# %%

f, ax = plt.subplots(1, figsize=(20, 20))
cats = ['Straßenraum begrünt', 'Straßenraum unbegrünt', 'Parkplätze u. Parkhäuser']
colors = ['k', 'k', 'k']
alphas = [0.5, 0.7, 0.5]
for cat, color, alpha in zip(cats, colors, alphas):
    geoplot.polyplot(df_realnut[df_realnut.NUTZUNG_LEVEL3 == cat], facecolor=color, ax=ax, alpha=alpha, lw=0)

# list(df_realnut)
# df_realnut.geometry

df_realnut_select = df_realnut[(df_realnut.NUTZUNG_LEVEL2 != 'Straßenraum') & (df_realnut.NUTZUNG_LEVEL3 != 'Parkplätze u. Parkhäuser')]
geoplot.polyplot(df_realnut_select, facecolor='white', ax=ax, lw=0)

for cat, color, alpha in zip(cats, colors, alphas):
    geoplot.polyplot(df_realnut[df_realnut.NUTZUNG_LEVEL3 == cat], facecolor=None, fill=False, ax=ax, alpha=alpha, lw=0.3)

plt.axis('off')
# plt.savefig('streets_lines.pdf')


# %%

f, ax = plt.subplots(1, figsize=(20, 20))
cats = ['Straßenraum begrünt', 'Straßenraum unbegrünt', 'Parkplätze u. Parkhäuser']
colors = ['k', 'k', 'k']
alphas = [0.5, 0.7, 0.5]
for cat, color, alpha in zip(cats, colors, alphas):
    df_realnut[df_realnut.NUTZUNG_LEVEL3 == cat].plot(ax=ax, color=color, alpha=alpha, lw=30)

df_realnut_select = df_realnut[(df_realnut.NUTZUNG_LEVEL2 != 'Straßenraum') & (df_realnut.NUTZUNG_LEVEL3 != 'Parkplätze u. Parkhäuser')]
df_realnut_select.plot(ax=ax, color='white')
plt.axis('off')

# plt.savefig('streets.pdf')


# %%

df = gpd.read_file(
    'https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:RADNETZOGD%20&srsName=EPSG:4326&outputFormat=json')

# bicycle

# erweitertes Grundnetz
df_select = df[df.M18_RANG_SUB == 'E']
ax = geoplot.sankey(df_select, ax=ax, lw=0.5, color='gray')

# Grundnetz
df_select = df[df.M18_RANG_SUB == 'G']
ax = geoplot.sankey(df_select, ax=ax, lw=0.6, color='black')

# Basisnetz
df_select = df[df.M18_RANG_SUB == 'B']
ax = geoplot.sankey(df_select, ax=ax, lw=0.9, color='gray')

# plt.savefig('bicycle2.pdf')

# %%
#
# streets and bike combined
#

separation_frac = 0.48
f, [ax1, ax2] = plt.subplots(nrows=1, figsize=(20, 20), ncols=2)

cats = ['Straßenraum begrünt', 'Straßenraum unbegrünt', 'Parkplätze u. Parkhäuser']
colors = ['k', 'k', 'k']
alphas = [0.5, 0.7, 0.5]
for cat, color, alpha in zip(cats, colors, alphas):
    geoplot.polyplot(df_realnut[df_realnut.NUTZUNG_LEVEL3 == cat], facecolor=color, ax=ax1, alpha=alpha, lw=0)

# list(df_realnut)
# df_realnut.geometry

df_realnut_select = df_realnut[(df_realnut.NUTZUNG_LEVEL2 != 'Straßenraum') & (df_realnut.NUTZUNG_LEVEL3 != 'Parkplätze u. Parkhäuser')]
geoplot.polyplot(df_realnut_select, facecolor='white', ax=ax1, lw=0)

# for cat, color, alpha in zip(cats, colors, alphas):
# geoplot.polyplot(df_realnut[df_realnut.NUTZUNG_LEVEL3 == cat], facecolor=None, fill=False, ax=ax1, alpha=alpha, lw=0.2)

# plt.axis('off')

xlim = ax1.axes.get_xlim()
ylim = ax1.axes.get_ylim()
xwidth = xlim[1] - xlim[0]

# patches = []
# polygon = Polygon(np.array([[xlim[0] + xwidth / 2, ylim[0]], [xlim[1], ylim[0]], [xlim[1], ylim[1]], [xlim[0] + xwidth / 2, ylim[1]]]), True)
# patches.append(polygon)
# p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
#
# ax.add_collection(p)

ax1.axes.set_xlim([xlim[0], xlim[0] + xwidth * separation_frac])

# bicycle

# erweitertes Grundnetz
df_select = df[df.M18_RANG_SUB == 'E']
ax = geoplot.sankey(df_select, ax=ax2, lw=0.2, color='gray')

# Grundnetz
df_select = df[df.M18_RANG_SUB == 'G']
ax = geoplot.sankey(df_select, ax=ax2, lw=0.35, color='black')

# Basisnetz
df_select = df[df.M18_RANG_SUB == 'B']
ax = geoplot.sankey(df_select, ax=ax2, lw=0.5, color='gray')

# Nebennetz
# df_select = df[df.M18_RANG_SUB == 'N']
# ax = geoplot.sankey(df_select, ax=ax2, lw=0.1, color='gray')

ax2.axes.set_xlim([xlim[0] + xwidth * separation_frac, xlim[1]])
ax2.axes.set_ylim(ylim)

plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig('street_bike_combined.pdf')

# %%
