import folium
import geopandas as gpd
import pandas as pd
import fiona
import datetime
map = folium.Map(location = [34, -95], zoom_start = 6, tiles = 'stamen toner')

#NaturalGas_ProcessingPlants_US_EIA = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/NaturalGas_ProcessingPlants_US_EIA.zip"
NaturalGas_InterIntrastate_Pipelines_US_EIA = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/NaturalGas_InterIntrastate_Pipelines_US_EIA.zip"
PowerPlants_US_EIA = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/PowerPlants_US_EIA.zip"
NERC_Regions_EIA = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/NERC_Regions_EIA.zip"
cb_2018_us_state_5m = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/cb_2018_us_state_5m.zip"
cb_2018_us_county_500k = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/cb_2018_us_county_500k.zip"
NaturalGas_UndergroundStorage_US_EIA = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/NaturalGas_UndergroundStorage_US_EIA.zip"
Electric_Power_Transmission_Lines = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/Electric_Power_Transmission_Lines.zip"
TightOil_ShaleGas_Plays_Lower48_EIA = "zip:///Users/liwatts/Documents/GitHub/Thesis/Code/TightOil_ShaleGas_Plays_Lower48_EIA.zip"

#ng_plants = gpd.read_file(NaturalGas_ProcessingPlants_US_EIA)
ng_plants = gpd.read_file('NaturalGas_ProcessingPlants_US_EIA.zip')
ng_plants_tx = ng_plants.loc[ng_plants['State'] == "TX"]

ng_pipes = gpd.read_file(NaturalGas_InterIntrastate_Pipelines_US_EIA)
ng_pipes_intra = ng_pipes.loc[ng_pipes['TYPEPIPE'] == 'Intrastate']
ng_pipes_tx = ng_pipes.loc[ng_pipes['Operator'] == "Kinder Morgan Texas Pipeline Co"]
ng_pipes_1 = ng_pipes_tx.loc[ng_pipes_tx['Shape_Leng'] == 0.0771166326871]
ng_pipes_intra_fix = ng_pipes_intra.dropna()

pwplants = gpd.read_file(PowerPlants_US_EIA)
df_pwplants = pd.DataFrame(pwplants)
pwplants_tx = pwplants.loc[pwplants['StateName'] == "Texas"]
pwplants_ng_tx = pwplants_tx.loc[pwplants_tx['NG_MW'] > 0.0]

pwplants_ng_tx['Plant_Name'] = pwplants_ng_tx['Plant_Name'].str.replace(' ', '')

pwplants_ng_tx = pwplants_ng_tx.reset_index()

regions = gpd.read_file(NERC_Regions_EIA)
regions_ercot = regions.loc[regions['NERC_Label'] == 'Texas Reliability Entity (TRE)']

states = gpd.read_file(cb_2018_us_state_5m)
tx_state = states.loc[states['NAME'] == 'Texas']

counties = gpd.read_file(cb_2018_us_county_500k)
tx_counties = counties.loc[counties['STATEFP'] == '48']

#derate = pd.read_excel(r'C:\Users\liwatts\Documents\GitHub\Thesis\Code\unit_outage.xlsx')

derate = pd.read_excel('unit_outage.xlsx')

derate_ng = derate.loc[derate['FUEL TYPE'] == 'NG']
derate_1 = derate.loc[derate['STATION LONG NAME'] == 'WA PARISH']
derate_1 = derate_1.loc[derate_1['FUEL TYPE'] == 'NG']
derate_1 = derate_1[:-1]
derate_1_G1 = derate_1.loc[derate_1['UNIT NAME'] == 'WAP_G1']
derate_1_G2 = derate_1.loc[derate_1['UNIT NAME'] == 'WAP_G2']
derate_1_G3 = derate_1.loc[derate_1['UNIT NAME'] == 'WAP_G3']
derate_1_G4 = derate_1.loc[derate_1['UNIT NAME'] == 'WAP_G4']


derate_ng['STATION LONG NAME'] = derate_ng['STATION LONG NAME'].str.replace(' ', '')

derate_ng['START'] = pd.to_datetime(derate_ng['START'])
derate_ng['END'] = pd.to_datetime(derate_ng['END'])

derate_1['START'] = pd.to_datetime(derate_1['START'])
derate_1['END'] = pd.to_datetime(derate_1['END'])

derate_1_G1['START'] = pd.to_datetime(derate_1_G1['START'])
derate_1_G1['END'] = pd.to_datetime(derate_1_G1['END'])

derate_1_G2['START'] = pd.to_datetime(derate_1_G2['START'])
derate_1_G2['END'] = pd.to_datetime(derate_1_G2['END'])

derate_1_G3['START'] = pd.to_datetime(derate_1_G3['START'])
derate_1_G3['END'] = pd.to_datetime(derate_1_G3['END'])

derate_1_G4['START'] = pd.to_datetime(derate_1_G4['START'])
derate_1_G4['END'] = pd.to_datetime(derate_1_G4['END'])

derate_ng = derate_ng.reset_index()
derate_1 = derate_1.reset_index()
derate_1_G1 = derate_1_G1.reset_index()
derate_1_G2 = derate_1_G2.reset_index()
derate_1_G3 = derate_1_G3.reset_index()
derate_1_G4 = derate_1_G4.reset_index()


ng_understorage = gpd.read_file(NaturalGas_UndergroundStorage_US_EIA)
ng_understorage_tx = ng_understorage.loc[ng_understorage['State'] == 'TX']

trans = gpd.read_file(Electric_Power_Transmission_Lines)

shale_plays = gpd.read_file(TightOil_ShaleGas_Plays_Lower48_EIA)




map = folium.Map(location = [34, -95], zoom_start = 6, tiles = 'cartodb positron')

style_1 = lambda x: {'color': '#ff0000', 'opacity': 0.1}
style_2 = lambda x: {'fillOpacity': 0.05}
style_3 = lambda x: {'color': '#000000','fillOpacity': 0, 'weight': 1}
style_4 = lambda x: {'color': '#000000','fillOpacity': 0, 'weight': 0.5}
style_5 = lambda x: {'color': '#cc8899', 'fillcolor': '#cc8899', 'fillOpacity': .2, 'weight': 2}

folium.GeoJson(data = regions_ercot['geometry'], style_function = style_2).add_to(map)
folium.GeoJson(data = tx_state['geometry'], style_function = style_3).add_to(map)
folium.GeoJson(data = tx_counties['geometry'], style_function = style_4).add_to(map)


for i in range (0, len(ng_pipes_tx)):
    feature = folium.features.GeoJson(
        ng_pipes_tx.iloc[[i]],
        style_function = style_1,
        tooltip = folium.features.GeoJsonTooltip(
            fields=[
                'Operator',
                'Shape_Leng',
            ]
        )
    )
    map.add_child(feature)
    map.keep_in_front(feature)

for i in range (0, len(shale_plays)):
    feature = folium.features.GeoJson(
        shale_plays.iloc[[i]],
        style_function = style_5,
        tooltip = folium.features.GeoJsonTooltip(
            fields=[
                'Basin',
                'Shale_play'
            ]
        )
    )
    map.add_child(feature)
    map.keep_in_front(feature)

for i in range (0, len(ng_plants_tx)):
    folium.CircleMarker(
        location=[ng_plants_tx.iloc[i]['Latitude'], ng_plants_tx.iloc[i]['Longitude']],
        tooltip = ng_plants_tx.iloc[i]['Plant_Name'],
        radius = float(ng_plants_tx.iloc[i]['BTU_Conten'])*.0075,
        color = 'crimson',
        fill = True,
        fill_color = 'crimson',
        weight = 0.5,
        fill_opacity = .6
    ).add_to(map)

for i in range (0, len(pwplants_ng_tx)):
    folium.CircleMarker(
        location = [pwplants_ng_tx.iloc[i]['Latitude'], pwplants_ng_tx.iloc[i]['Longitude']],
        tooltip = pwplants_ng_tx.iloc[i]['Plant_Name'],
        radius = float(pwplants_ng_tx.iloc[i]['Total_MW'])*.015,
        color = 'steelblue',
        fill = True,
        fill_color = 'steelblue',
        weight = 0.5,
        fill_opacity = .6
    ).add_to(map)

for i in range (0, len(ng_understorage_tx)):
    folium.CircleMarker(
        location = [ng_understorage_tx.iloc[i]['Latitude'], ng_understorage_tx.iloc[i]['Longitude']],
        tooltip = ng_understorage_tx.iloc[i]['Field'],
        radius = float(ng_understorage_tx.iloc[i]['maxdeliv'])*.0000075,
        color = 'Green',
        fill = True,
        fill_color = 'Green',
        weight = 0.5,
        fill_opacity = .6
    ).add_to(map)

#map.save('simple_static_map.html')