import folium
import geopandas as gpd
import pandas as pd
import datetime

map = folium.Map(location=[34, -95], zoom_start=6, tiles="stamen toner")


ng_plants = gpd.read_file("NaturalGas_ProcessingPlants_US_EIA.zip")
ng_plants_tx = ng_plants.loc[ng_plants["State"] == "TX"]

ng_pipes = gpd.read_file("NaturalGas_InterIntrastate_Pipelines_US_EIA.zip")
ng_pipes_intra = ng_pipes.loc[ng_pipes["TYPEPIPE"] == "Intrastate"]
ng_pipes_tx = ng_pipes.loc[ng_pipes["Operator"] == "Kinder Morgan Texas Pipeline Co"]
ng_pipes_1 = ng_pipes_tx.loc[ng_pipes_tx["Shape_Leng"] == 0.0771166326871]
ng_pipes_intra_fix = ng_pipes_intra.dropna()
ng_pipes_intra_fix = ng_pipes_intra_fix.reset_index()

pwplants = gpd.read_file("PowerPlants_US_EIA.zip")
df_pwplants = pd.DataFrame(pwplants)
pwplants_tx = pwplants.loc[pwplants["StateName"] == "Texas"]
pwplants_ng_tx = pwplants_tx.loc[pwplants_tx["NG_MW"] > 0.0]

pwplants_ng_tx["Plant_Name"] = pwplants_ng_tx["Plant_Name"].str.replace(" ", "")

pwplants_ng_tx = pwplants_ng_tx.reset_index()

regions = gpd.read_file("NERC_Regions_EIA.zip")
regions_ercot = regions.loc[regions["NERC_Label"] == "Texas Reliability Entity (TRE)"]

states = gpd.read_file("cb_2018_us_state_5m.zip")
tx_state = states.loc[states["NAME"] == "Texas"]

counties = gpd.read_file("cb_2018_us_county_500k.zip")
tx_counties = counties.loc[counties["STATEFP"] == "48"]

derate = pd.read_excel("unit_outage.xlsx")
derate_ng = derate.loc[derate["FUEL TYPE"] == "NG"]
derate_1 = derate.loc[derate["STATION LONG NAME"] == "WA PARISH"]
derate_1 = derate_1.loc[derate_1["FUEL TYPE"] == "NG"]
derate_1 = derate_1[:-1]


derate_ng["STATION LONG NAME"] = derate_ng["STATION LONG NAME"].str.replace(" ", "")

derate_ng["START"] = pd.to_datetime(derate_ng["START"])
derate_ng["END"] = pd.to_datetime(derate_ng["END"])

derate_1["START"] = pd.to_datetime(derate_1["START"])
derate_1["END"] = pd.to_datetime(derate_1["END"])

derate_ng = derate_ng.reset_index()
derate_1 = derate_1.reset_index()

ng_understorage = gpd.read_file("NaturalGas_UndergroundStorage_US_EIA.zip")
ng_understorage_tx = ng_understorage.loc[ng_understorage["State"] == "TX"]

trans = gpd.read_file("Electric_Power_Transmission_Lines.zip")

shale_plays = gpd.read_file("TightOil_ShaleGas_Plays_Lower48_EIA.zip")
shale_plays_tx = shale_plays[
    shale_plays["Shale_play"].str.contains(
        "Barnett|Bend|Abo-Yeso|Delaware|Wolfcamp|Wolfcamp-Midland|Spraberry|Eagle Ford|Haynesville-Bossier"
    )
]


lat = [0] * len(derate_ng)
lon = [0] * len(derate_ng)
capacity = [0] * len(derate_ng)

derate_ng["STATION LONG NAME"].replace(" ", "")

for i in range(len(derate_ng)):

    if derate_ng["STATION LONG NAME"][i] == "LAREDOENERGYCENTER":
        lat[i] = 27.5667
        lon[i] = -99.5089
        capacity[i] = 177.4

    if derate_ng["STATION LONG NAME"][i] == "ANTELOPEELKENERGYCENTER":
        lat[i] = 33.865
        lon[i] = -101.843333
        capacity[i] = 158.9

    if derate_ng["STATION LONG NAME"][i] == "CALAVERAS":
        lat[i] = 29.308
        lon[i] = -98.32
        capacity[i] = 830.0

    if derate_ng["STATION LONG NAME"][i] == "HANDLEYSES":
        lat[i] = 32.7283
        lon[i] = -97.2192
        capacity[i] = 1265.0

    if derate_ng["STATION LONG NAME"][i] == "STRYKERCREEKSES":
        lat[i] = 31.93985
        lon[i] = -94.98983
        capacity[i] = 669.0

    if derate_ng["STATION LONG NAME"][i] == "MILLER":
        lat[i] = 32.6581
        lon[i] = -98.3103
        capacity[i] = 574.0

    if derate_ng["STATION LONG NAME"][i] == "ODESSAECTORCCS":
        lat[i] = 31.8403
        lon[i] = -102.3264
        capacity[i] = 1061.8

    if derate_ng["STATION LONG NAME"][i] == "WOLFHOLLOWGEN":
        lat[i] = 32.334220
        lon[i] = -97.731686
        capacity[i] = 750.5

    if derate_ng["STATION LONG NAME"][i] == "MOUNTAINCREEKSES":
        lat[i] = 32.7231
        lon[i] = -96.9358
        capacity[i] = 826.0

    if derate_ng["STATION LONG NAME"][i] == "BARNEYDAVIS":
        lat[i] = 27.6064
        lon[i] = -97.3117
        capacity[i] = 925.0

    if derate_ng["STATION LONG NAME"][i] == "SANJACINTOSTEAM":
        lat[i] = 29.694838
        lon[i] = -95.040622
        capacity[i] = 162.0

    if derate_ng["STATION LONG NAME"][i] == "SAMRAYBURNSWITCHYD":
        lat[i] = 28.8947
        lon[i] = -97.135
        capacity[i] = 204.0

    if derate_ng["STATION LONG NAME"][i] == "BRAUNIG":
        lat[i] = 29.256700
        lon[i] = -98.382500
        capacity[i] = 1050.0

    if derate_ng["STATION LONG NAME"][i] == "NORTHEDINBURG":
        lat[i] = 26.34172
        lon[i] = -98.175759
        capacity[i] = 470.0

    if derate_ng["STATION LONG NAME"][i] == "TENASKA(TXU)":
        lat[i] = 32.017826
        lon[i] = -94.619743
        capacity[i] = 845.0

    if derate_ng["STATION LONG NAME"][i] == "DECORDOVASES":
        lat[i] = 32.403056
        lon[i] = -97.700556
        capacity[i] = 282.0

    if derate_ng["STATION LONG NAME"][i] == "KIAMICHIENERGYFACILITY":
        lat[i] = 33.587
        lon[i] = -96.118
        capacity[i] = 1220.0

    if derate_ng["STATION LONG NAME"][i] == "PANDATEMPLEPOWERII":
        lat[i] = 31.055833
        lon[i] = -97.317222
        capacity[i] = 1503.0

    if derate_ng["STATION LONG NAME"][i] == "HAYSENERGY":
        lat[i] = 29.7806
        lon[i] = -97.9894
        capacity[i] = 912.0

    if derate_ng["STATION LONG NAME"][i] == "BOSQUESWITCH":
        lat[i] = 31.8594
        lon[i] = -97.3586
        capacity[i] = 758.0

    if derate_ng["STATION LONG NAME"][i] == "FRONTIER":
        lat[i] = 30.5924
        lon[i] = -95.9178
        capacity[i] = 860.0

    if derate_ng["STATION LONG NAME"][i] == "TENASKA(BRAZOS)":
        lat[i] = 32.017826
        lon[i] = -94.619743
        capacity[i] = 845.0

    if derate_ng["STATION LONG NAME"][i] == "FORMOSA":
        lat[i] = 28.6917
        lon[i] = -96.5417
        capacity[i] = 597.3

    if derate_ng["STATION LONG NAME"][i] == "REDGATE":
        lat[i] = 26.451111
        lon[i] = -98.1775
        capacity[i] = 219.6

    if derate_ng["STATION LONG NAME"][i] == "BRAZOSVALLEYENERGY":
        lat[i] = 29.4723
        lon[i] = -95.62301
        capacity[i] = 1076.0

    if derate_ng["STATION LONG NAME"][i] == "SANDHILLENERGYCTR":
        lat[i] = 30.2098
        lon[i] = -97.6129
        capacity[i] = 595.8

    if derate_ng["STATION LONG NAME"][i] == "CALHOUNSUBSTATION":
        lat[i] = 28.64807
        lon[i] = -96.54621
        capacity[i] = 86.0

    if derate_ng["STATION LONG NAME"][i] == "CHANNELVIEWCOGEN":
        lat[i] = 29.836952
        lon[i] = -95.121744
        capacity[i] = 782.0

    if derate_ng["STATION LONG NAME"][i] == "DECKERPOWERPLANT":
        lat[i] = 30.3033
        lon[i] = -97.6128
        capacity[i] = 612.0

    if derate_ng["STATION LONG NAME"][i] == "DOW":
        lat[i] = 28.988
        lon[i] = -95.38
        capacity[i] = 678.1

    if derate_ng["STATION LONG NAME"][i] == "AMOCOOILCOGEN":
        lat[i] = 29.37
        lon[i] = -94.93
        capacity[i] = 1055.0

    if derate_ng["STATION LONG NAME"][i] == "PASGEN":
        lat[i] = 29.72475
        lon[i] = -95.176479
        capacity[i] = 720.0

    if derate_ng["STATION LONG NAME"][i] == "BRYN_DANSBY":
        lat[i] = 30.7217
        lon[i] = -96.4608
        capacity[i] = 204.2

    if derate_ng["STATION LONG NAME"][i] == "LOSTPINES":
        lat[i] = 30.1478
        lon[i] = -97.2714
        capacity[i] = 510.0

    if derate_ng["STATION LONG NAME"][i] == "QUAILSWITCH":
        lat[i] = 31.8414
        lon[i] = -102.315
        capacity[i] = 472.2

    if derate_ng["STATION LONG NAME"][i] == "CEDARBAYOUPLANT":
        lat[i] = 29.750000
        lon[i] = -94.92560
        capacity[i] = 1495.0

    if derate_ng["STATION LONG NAME"][i] == "MIDLOTHIANANP":
        lat[i] = 32.4302
        lon[i] = -97.0537
        capacity[i] = 1560.0

    if derate_ng["STATION LONG NAME"][i] == "GUADALUPEGEN":
        lat[i] = 29.6244
        lon[i] = -98.1419
        capacity[i] = 1011.6

    if derate_ng["STATION LONG NAME"][i] == "MORGANCREEKSES":
        lat[i] = 32.3358
        lon[i] = -100.9156
        capacity[i] = 402.0

    if derate_ng["STATION LONG NAME"][i] == "BAYOUCOGEN":
        lat[i] = 29.6225
        lon[i] = -95.0458
        capacity[i] = 300.0

    if derate_ng["STATION LONG NAME"][i] == "JACKCOUNTY2PLANT":
        lat[i] = 33.1010
        lon[i] = -97.9574
        capacity[i] = 1241.0

    if derate_ng["STATION LONG NAME"][i] == "GRAHAMSES":
        lat[i] = 33.1344
        lon[i] = -98.6117
        capacity[i] = 624.0

    for k in range(len(pwplants_ng_tx)):

        if (
            derate_ng["STATION LONG NAME"][i].lower()
            == pwplants_ng_tx["Plant_Name"][k].lower()
        ):
            lat[i] = pwplants_ng_tx["Latitude"][k]
            lon[i] = pwplants_ng_tx["Longitude"][k]
            capacity[i] = pwplants_ng_tx["NG_MW"][k]

derate_ng["latitude"] = lat
derate_ng["longitude"] = lon
derate_ng["capacity"] = capacity

derate_ng.loc[derate_ng["capacity"] == 0]

derate_ng = derate_ng[derate_ng.capacity != 0]

derate_slim = derate_ng.drop_duplicates(subset=["STATION LONG NAME"])

derate_slim = derate_slim.reset_index()
derate_ng = derate_ng.reset_index()


df_2 = pd.DataFrame(columns=["timeframe", "Plant", "Latitude", "Longitude", "Capacity"])

timeframe = pd.DatetimeIndex([])
plant = []
latitude = []
longitude = []
capacity = []

for i in range(len(derate_slim)):
    timeframe = timeframe.append(pd.date_range("2021-02-14", "2021-02-20", periods=865))

    for k in range(0, 865):
        plant.append(derate_slim["STATION LONG NAME"][i])
        latitude.append(derate_slim["latitude"][i])
        longitude.append(derate_slim["longitude"][i])
        capacity.append(derate_slim["capacity"][i])

for k in range(len(derate_ng)):

    for i in range(len(timeframe)):

        if derate_ng["STATION LONG NAME"][k] == plant[i]:

            if derate_ng["END"][k] > timeframe[i] >= derate_ng["START"][k]:

                capacity[i] = (
                    capacity[i] - derate_ng["MW REDUCTION FROM OUTAGE/DERATE"][k]
                )

df_2 = pd.DataFrame(
    list(zip(timeframe, plant, latitude, longitude, capacity)),
    columns=["time", "plant_name", "latitude", "longitude", "capacity"],
)


map = folium.Map(location=[34, -95], zoom_start=6, tiles="cartodb positron")

style_1 = lambda x: {"color": "#ff0000", "opacity": 0.2, "weight": 2}
style_2 = lambda x: {"fillOpacity": 0.05}
style_3 = lambda x: {"color": "#000000", "fillOpacity": 0, "weight": 1}
style_4 = lambda x: {
    "color": "#000000",
    "fillOpacity": 0,
    "weight": 0.3,
    "opacity": 0.5,
}
style_5 = lambda x: {
    "color": "#cc8899",
    "fillcolor": "#cc8899",
    "fillOpacity": 0.3,
    "weight": 0,
}

folium.GeoJson(data=regions_ercot["geometry"], style_function=style_2).add_to(map)
folium.GeoJson(data=tx_state["geometry"], style_function=style_3).add_to(map)
folium.GeoJson(data=tx_counties["geometry"], style_function=style_4).add_to(map)
# folium.GeoJson(data = trans['geometry']).add_to(map)

for i in range(0, len(ng_pipes_intra_fix)):

    if ng_pipes_intra_fix["Operator"][i] == "Kinder Morgan Texas Pipeline Co":

        feature = folium.features.GeoJson(
            ng_pipes_intra_fix.iloc[[i]],
            style_function=style_1,
            tooltip=folium.features.GeoJsonTooltip(
                fields=[
                    "Operator",
                    "Shape_Leng",
                ]
            ),
        )
        map.add_child(feature)
        map.keep_in_front(feature)

    if ng_pipes_intra_fix["Operator"][i] == "Crosstex Texas Systems":

        feature = folium.features.GeoJson(
            ng_pipes_intra_fix.iloc[[i]],
            style_function=style_1,
            tooltip=folium.features.GeoJsonTooltip(
                fields=[
                    "Operator",
                    "Shape_Leng",
                ]
            ),
        )
        map.add_child(feature)
        map.keep_in_front(feature)


for i in range(0, len(shale_plays_tx)):
    feature = folium.features.GeoJson(
        shale_plays_tx.iloc[[i]],
        style_function=style_5,
        tooltip=folium.features.GeoJsonTooltip(fields=["Basin", "Shale_play"]),
    )
    map.add_child(feature)
    map.keep_in_front(feature)

for i in range(0, len(ng_plants_tx)):
    folium.CircleMarker(
        location=[ng_plants_tx.iloc[i]["Latitude"], ng_plants_tx.iloc[i]["Longitude"]],
        tooltip=ng_plants_tx.iloc[i]["Plant_Name"],
        radius=float(ng_plants_tx.iloc[i]["BTU_Conten"]) * 0.0075,
        color="crimson",
        fill=True,
        fill_color="crimson",
        weight=0.5,
        fill_opacity=0.6,
    ).add_to(map)

# for i in range (0, len(pwplants_ng_tx)):
#    folium.CircleMarker(
#        location = [pwplants_ng_tx.iloc[i]['Latitude'], pwplants_ng_tx.iloc[i]['Longitude']],
#        tooltip = pwplants_ng_tx.iloc[i]['Plant_Name'],
#        radius = float(pwplants_ng_tx.iloc[i]['Total_MW'])*.015,
#        color = 'steelblue',
#        fill = True,
#        fill_color = 'steelblue',
#        weight = 0.5,
#        fill_opacity = .6
#    ).add_to(map)

for i in range(0, len(ng_understorage_tx)):
    folium.CircleMarker(
        location=[
            ng_understorage_tx.iloc[i]["Latitude"],
            ng_understorage_tx.iloc[i]["Longitude"],
        ],
        tooltip=ng_understorage_tx.iloc[i]["Field"],
        radius=float(ng_understorage_tx.iloc[i]["maxdeliv"]) * 0.0000075,
        color="Green",
        fill=True,
        fill_color="Green",
        weight=0.5,
        fill_opacity=0.6,
    ).add_to(map)


import folium.plugins as plugins

ng_pipes_intra_fix_2 = ng_pipes_intra_fix.explode()

ng_pipes_intra_fix_3 = ng_pipes_intra_fix_2[
    ng_pipes_intra_fix_2["Operator"].str.contains("Kinder")
]
ng_pipes_intra_fix_3 = ng_pipes_intra_fix_3[ng_pipes_intra_fix_3["Shape_Leng"] > 0.03]

stufftest = list(ng_pipes_intra_fix_3["geometry"])

testing_1 = [list(x.coords) for x in stufftest]

ant_coord = []

for i in range(len(testing_1)):

    for k in range(2):

        ant_coord.append([testing_1[i][k][1], testing_1[i][k][0]])


for i in range(0, len(ant_coord) - 2, 2):

    folium.plugins.AntPath(
        locations=ant_coord[i : i + 2],
        color="green",
        delay=2000,
        dashArray=[10, 20],
        weight=5,
        pulseColor="#FF00FF",
        # tooltip = ng_pipes_intra_fix_3.iloc[i]['Operator'],
        # paused = True,
        hardwareAccelerated=True,
    ).add_to(map)


def create_geojson_features(df_2):

    features = []
    for lat, lon, capacity, time in zip(
        df_2["latitude"], df_2["longitude"], df_2["capacity"], df_2["time"]
    ):
        time = str(time)
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "time": time,
                "icon": "circle",
                "color": "steelblue",
                "iconstyle": {
                    "color": "steelblue",
                    "fillOpacity": 0.5,
                    "stroke": False,
                    "radius": capacity * 0.015,
                },
            },
        }
        features.append(feature)
        feature = {
            "type": "Feature",
            "geometry": {"type": "Linestring", "coordinates": [-106.375, 31.7690]},
            "properties": {
                "name": "capacity",
                "time": time,
                "icon": "circle",
                "color": "steelblue",
                "iconstyle": {
                    "color": "steelblue",
                    "fillOpacity": 0.6,
                    "stroke": "false",
                    "radius": capacity * 0.05,
                },
            },
        }
        features.append(feature)

    return features


features = create_geojson_features(df_2)

from folium.plugins import TimestampedGeoJson

# map = folium.Map(location = [34, -95], zoom_start = 6, tiles = 'cartodb positron')

TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="PT10M",
    duration="PT10M",
    add_last_point=False,
    auto_play=False,
    transition_time=200,
    loop=False,
    max_speed=50,
    loop_button=True,
    date_options="YYYY/MM/DD HH:mm:ss",
    time_slider_drag_update=True,
).add_to(map)

map.save("simple_animation_map.html")
