# street and bicycle map

import matplotlib.pyplot as plt
import geopandas as gpd
import geoplot

# %%

wien = gpd.read_file('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:BEZIRKSGRENZEOGD&srsName=EPSG:4326&outputFormat=json')

df_realnut = gpd.read_file('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:REALNUT2018OGD%20&srsName=EPSG:4326&outputFormat=json')

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
