'''
	plot_map.py

	Schritt 4 bei der Ermittlung der
	Waldpreise in Deutschland.

	Programm, um Preise und Lagen für
	Waldgebote auf einer Deutschlandkarte
	einzuzeichnen.

	Nutzt die datrei: lagen_aww.csv

	Dezember 2018
	Aktualisiert Dezember 2019
'''

import pandas as pd
import geopandas
import matplotlib.pyplot as plt


lagen = pd.read_csv('lagen_aww.csv', delimiter = ';')
lagen_T0 = lagen[lagen['ART'] == 'T0']
lagen_T1= lagen[lagen['ART'] == 'T1']
lagen_T2= lagen[lagen['ART'] == 'T2']
lagen_T3= lagen[lagen['ART'] == 'T3']
lagen_T4= lagen[lagen['ART'] == 'T4']
lagen_T5= lagen[lagen['ART'] == 'T5']
lagen_T6= lagen[lagen['ART'] == 'T6']

gdf_T0 = geopandas.GeoDataFrame(lagen_T0, geometry=geopandas.points_from_xy(lagen_T0.LON, lagen_T0.LAT))
gdf_T1 = geopandas.GeoDataFrame(lagen_T1, geometry=geopandas.points_from_xy(lagen_T1.LON, lagen_T1.LAT))
gdf_T2 = geopandas.GeoDataFrame(lagen_T2, geometry=geopandas.points_from_xy(lagen_T2.LON, lagen_T2.LAT))
gdf_T3 = geopandas.GeoDataFrame(lagen_T3, geometry=geopandas.points_from_xy(lagen_T3.LON, lagen_T3.LAT))
gdf_T4 = geopandas.GeoDataFrame(lagen_T4, geometry=geopandas.points_from_xy(lagen_T4.LON, lagen_T4.LAT))
gdf_T5 = geopandas.GeoDataFrame(lagen_T5, geometry=geopandas.points_from_xy(lagen_T5.LON, lagen_T5.LAT))
gdf_T6 = geopandas.GeoDataFrame(lagen_T6, geometry=geopandas.points_from_xy(lagen_T6.LON, lagen_T6.LAT))

deutschland = geopandas.read_file("4_niedrig.geojson")
#https://matplotlib.org/3.1.0/gallery/color/named_colors.html
ax = deutschland.plot(color='white', edgecolor='black')
gdf_T0.plot(ax=ax, color='darkgreen', markersize = 10, label="1-1.99€/qm")
gdf_T1.plot(ax=ax, color='limegreen', markersize = 20, label = "2-2.99€/qm")
gdf_T2.plot(ax=ax, color='navy', markersize = 30, label = "3-3.99€/qm")
gdf_T3.plot(ax=ax, color='violet' , markersize = 40, label="4-4.99€/qm")
gdf_T4.plot(ax=ax, color='cornflowerblue', markersize = 50, label = "5-5.99€/qm")
gdf_T5.plot(ax=ax, color='yellow', markersize = 60, label = "6-6.99€/qm")
gdf_T6.plot(ax=ax, color='red', markersize = 70, label = "7€ und mehr/qm")
ax.legend(loc="top left", title="", frameon=False)


plt.show()