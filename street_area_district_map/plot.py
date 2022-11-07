import geopandas as gpd
import geoplot
import matplotlib
import matplotlib.font_manager
import matplotlib.pyplot as plt
# for latex fonts
from matplotlib import rc

rc('text', usetex=True)
# rc('text.latex', preamble=r'')
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Sans serif']})
matplotlib.rcParams['text.color'] = '#515c50'


# %%

wien = gpd.read_file(
    'https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:BEZIRKSGRENZEOGD&srsName=EPSG:4326&outputFormat=json')

# 2018
# df_realnut = gpd.read_file('https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:REALNUT2018OGD%20&srsName=EPSG:4326&outputFormat=json')

# 2020
df_realnut = gpd.read_file(
    'https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:REALNUT2020OGD')

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


f, ax = plt.subplots(1, figsize=(25, 25))
# geoplot.polyplot(wien, ax=ax, color='#a2c865', alpha=0.3)
geoplot.polyplot(wien, ax=ax, color='#95a3c3', alpha=0.1)
ax = geoplot.cartogram(
    wien, scale='street', scale_func=identity_scale, limits=(0, 1),
    # edgecolor='None', ax=ax, color='#8690ad', alpha=0.95
    edgecolor='None', ax=ax, color='#95a3c3', alpha=0.95
)
geoplot.polyplot(wien, edgecolor='gray', ax=ax, lw=1)
plt.hist([], histtype='stepfilled', color='#95a3c3', alpha=0.95, label=' Straßen \& Parkplätze', lw=3)
plt.hist([], histtype='stepfilled', fc=(149 / 255, 163 / 255, 195 / 255, 0.1), label=' Andere Nutzung', lw=3, edgecolor='gray')
plt.legend(loc='lower center', fontsize=46, frameon=False, ncol=2, bbox_to_anchor=[0, -0.12, 1, 1])
plt.tight_layout()
plt.savefig('./poster_street_area/streetarea_districts_legend_blue.pdf')

# %%
