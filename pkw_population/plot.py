import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import os

#%%

df = pd.read_csv('https://www.wien.gv.at/gogv/l9ogdpkwbevoelkerungbezirke2017', sep=';')
df = df.query('YEAR == 2017')

district_map = {'Wien Alsergrund': 9,
                'Wien Mariahilf': 6,
                'Wien Landstraße': 3,
                'Wien Leopoldstadt': 1,
                'Wien Liesing': 23,
                'Wien Wieden': 5,
                'Wien Favoriten': 10,
                'Wien Margareten': 4,
                'Wien Rudolfsheim-Fünfhaus': 15,
                'Wien Donaustadt': 22,
                'Wien Brigittenau': 20,
                'Wien Neubau': 7,
                'Wien Döbling': 19,
                'Wien Innere Stadt': 1,
                'Wien Ottakring': 16,
                'Wien Josefstadt': 8,
                'Wien Währing': 18,
                'Wien Penzing': 14,
                'Wien Hernals': 17,
                'Wien Hietzing': 13,
                'Wien Floridsdorf': 21,
                'Wien Meidling': 12,
                'Wien Simmering': 11}

df = df.sort_values(by='POPULATION', ascending=False)
for i in range(len(df)):
    entry = df.iloc[i]
    dist = entry.DISTRICT
    cars = entry.PASSENGER_CARS
    pop = entry.POPULATION
    print(dist, cars / pop)

#%%

plt.rcParams['figure.figsize'] = (16, 6)
plt.rcParams['font.size'] = 16

x_pos = np.arange(1, 24)
width = 0.8
plt.bar(x_pos, df.POPULATION.values, width=width, label='Bevölkerung')
plt.bar(x_pos, df.PASSENGER_CARS.values, alpha=0.9, width=width, label='PKW')
plt.ylabel('Anzahl')
plt.xticks(x_pos, df.DISTRICT.values, rotation=85)  # Set text labels and properties.
plt.legend()


#%%

os.system('mkdir -p pkw_population/per_district')
districts = [dist[5:] for dist in df.DISTRICT.values]

fig = go.Figure(data=[
    go.Bar(name='Bevölkerung', y=districts, x=df.POPULATION.values, orientation='h'),
    go.Bar(name='PKW', y=districts, x=df.PASSENGER_CARS.values, text=[f'{ratio * 100:{.2}f}%' for ratio in df.PASSENGER_CARS.values / df.POPULATION.values], textposition='inside', orientation='h', textfont=dict(color='white', size=16))
])
fig.update_layout(barmode='overlay', yaxis_tickangle=0)
fig.update_layout(
    xaxis_tickfont_size=14,
    xaxis=dict(
        title='Anzahl',
        titlefont_size=18,
        tickfont_size=16,
    ),
    yaxis=dict(
        titlefont_size=18,
        tickfont_size=16,
        ticksuffix=' '
    ),
    legend=dict(
        x=1.0,
        y=1.0,
        xanchor='right',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)',
        font=dict(size=16)
    ),
    bargap=0.2,  # gap between bars of adjacent location coordinates.
)
fig.update_layout(autosize=True)
pio.write_html(fig, file='pkw_population/per_district/index.html', auto_open=False, include_plotlyjs="cdn")  # , include_mathjax="cdn")
fig.show()

#%%
