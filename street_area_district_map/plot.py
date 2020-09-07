import matplotlib.pyplot as plt
import geopandas as gpd
import geoplot


# %%

wien = gpd.read_file('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:BEZIRKSGRENZEOGD&srsName=EPSG:4326&outputFormat=json')

df_realnut = gpd.read_file('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:REALNUT2018OGD%20&srsName=EPSG:4326&outputFormat=json')


# %%

df_realnut.BEZ = df_realnut.BEZ.astype('int')
df_select = df_realnut[(df_realnut.NUTZUNG_LEVEL2 == 'Straßenraum') | (df_realnut.NUTZUNG_LEVEL3 == 'Parkplätze u. Parkhäuser')]


district_dict = {}
for i in range(23):
    streets = df_select[(df_select.BEZ == i + 1)].FLAECHE.sum()
    district1 = df_realnut[df_realnut.BEZ == i + 1].FLAECHE.sum()
    district = wien[wien.BEZNR == i + 1].FLAECHE.item()
    print(abs(district1 - district) / district1)
    frac = (streets) / district
    district_dict[i + 1] = frac
    print(i + 1, float(frac))

wien['street'] = wien.BEZNR.map(district_dict)**(1 / 2)

# %%


def identity_scale(minval, maxval):
    def scalar(val):
        return val
    return scalar


f, ax = plt.subplots(1, figsize=(20, 20))
geoplot.polyplot(wien, ax=ax, color='green', alpha=0.1)
ax = geoplot.cartogram(
    wien, scale='street', scale_func=identity_scale, limits=(0, 1),
    edgecolor='None', figsize=(7, 8), ax=ax, color='black', alpha=0.7
)
geoplot.polyplot(wien, edgecolor='gray', ax=ax)


list(wien)

# %%
