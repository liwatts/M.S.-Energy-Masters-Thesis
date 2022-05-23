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
derate_1_G1 = derate_1.loc[derate_1["UNIT NAME"] == "WAP_G1"]
derate_1_G2 = derate_1.loc[derate_1["UNIT NAME"] == "WAP_G2"]
derate_1_G3 = derate_1.loc[derate_1["UNIT NAME"] == "WAP_G3"]
derate_1_G4 = derate_1.loc[derate_1["UNIT NAME"] == "WAP_G4"]


derate_ng["STATION LONG NAME"] = derate_ng["STATION LONG NAME"].str.replace(" ", "")

derate_ng["START"] = pd.to_datetime(derate_ng["START"])
derate_ng["END"] = pd.to_datetime(derate_ng["END"])

derate_1["START"] = pd.to_datetime(derate_1["START"])
derate_1["END"] = pd.to_datetime(derate_1["END"])

derate_1_G1["START"] = pd.to_datetime(derate_1_G1["START"])
derate_1_G1["END"] = pd.to_datetime(derate_1_G1["END"])

derate_1_G2["START"] = pd.to_datetime(derate_1_G2["START"])
derate_1_G2["END"] = pd.to_datetime(derate_1_G2["END"])

derate_1_G3["START"] = pd.to_datetime(derate_1_G3["START"])
derate_1_G3["END"] = pd.to_datetime(derate_1_G3["END"])

derate_1_G4["START"] = pd.to_datetime(derate_1_G4["START"])
derate_1_G4["END"] = pd.to_datetime(derate_1_G4["END"])

derate_ng = derate_ng.reset_index()
derate_1 = derate_1.reset_index()
derate_1_G1 = derate_1_G1.reset_index()
derate_1_G2 = derate_1_G2.reset_index()
derate_1_G3 = derate_1_G3.reset_index()
derate_1_G4 = derate_1_G4.reset_index()


ng_understorage = gpd.read_file("NaturalGas_UndergroundStorage_US_EIA.zip")
ng_understorage_tx = ng_understorage.loc[ng_understorage["State"] == "TX"]

trans = gpd.read_file("Electric_Power_Transmission_Lines.zip")

shale_plays = gpd.read_file("TightOil_ShaleGas_Plays_Lower48_EIA.zip")
shale_plays_tx = shale_plays[
    shale_plays["Shale_play"].str.contains(
        "Barnett|Bend|Abo-Yeso|Delaware|Wolfcamp|Wolfcamp-Midland|Spraberry|Eagle Ford|Haynesville-Bossier"
    )
]


map = folium.Map(location=[34, -95], zoom_start=6, tiles="cartodbdark_matter")

style_1 = lambda x: {"color": "#ff8f80", "opacity": 0.8}
style_2 = lambda x: {"color": "#c1e4f7", "fillOpacity": 0}
# style_3 = lambda x: {"color": "#000000", "fillOpacity": 0, "weight": 1}
style_3 = lambda x: {"color": "#FFFFFF", "fillOpacity": 0, "weight": 1}
# style_4 = lambda x: {"color": "#000000", "fillOpacity": 0, "weight": 0.5}
style_4 = lambda x: {"color": "#FFFFFF", "fillOpacity": 0, "weight": 0.5}
style_5 = lambda x: {
    "color": "#ff8f80",
    "fillcolor": "#ff8f80",
    "fillOpacity": 0.3,
    "weight": 2,
}

folium.GeoJson(data=regions_ercot["geometry"], style_function=style_2).add_to(map)
folium.GeoJson(data=tx_state["geometry"], style_function=style_3).add_to(map)
folium.GeoJson(data=tx_counties["geometry"], style_function=style_4).add_to(map)


for i in range(0, len(ng_pipes_tx)):
    feature = folium.features.GeoJson(
        ng_pipes_tx.iloc[[i]],
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
    # map.keep_in_front(feature)

for i in range(0, len(ng_plants_tx)):
    folium.CircleMarker(
        location=[ng_plants_tx.iloc[i]["Latitude"], ng_plants_tx.iloc[i]["Longitude"]],
        tooltip=ng_plants_tx.iloc[i]["Plant_Name"],
        radius=float(ng_plants_tx.iloc[i]["BTU_Conten"]) * 0.0075,
        color="#d1bcd2",
        fill=True,
        fill_color="#d1bcd2",
        weight=0.5,
        fill_opacity=1,
    ).add_to(map)

for i in range(0, len(pwplants_ng_tx)):
    folium.CircleMarker(
        location=[
            pwplants_ng_tx.iloc[i]["Latitude"],
            pwplants_ng_tx.iloc[i]["Longitude"],
        ],
        tooltip=pwplants_ng_tx.iloc[i]["Plant_Name"],
        radius=float(pwplants_ng_tx.iloc[i]["Total_MW"]) * 0.015,
        color="#c1e4f7",
        fill=True,
        fill_color="#c1e4f7",
        weight=0.5,
        fill_opacity=1,
    ).add_to(map)

for i in range(0, len(ng_understorage_tx)):
    folium.CircleMarker(
        location=[
            ng_understorage_tx.iloc[i]["Latitude"],
            ng_understorage_tx.iloc[i]["Longitude"],
        ],
        tooltip=ng_understorage_tx.iloc[i]["Field"],
        radius=float(ng_understorage_tx.iloc[i]["maxdeliv"]) * 0.0000075,
        color="#c7e8ac",
        fill=True,
        fill_color="#c7e8ac",
        weight=0.5,
        fill_opacity=1,
    ).add_to(map)

map.save("simple_static_map.html")
