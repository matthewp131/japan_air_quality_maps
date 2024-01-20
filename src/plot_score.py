import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

with open('../output/score_with_gps_6_pollutants.xlsx', 'rb') as f:
    df = pd.read_excel(f)

df = df.loc[df['total_score'].notna()]

df['text'] = df['full_address'].astype(str) + '<br>Score ' + df['total_score'].astype(str)
df['size'] = 0.1
df['hover_data'] = '<br>NMHC: ' + df['NMHC'].astype(str) + '<br>' + 'NO2: ' + df['NO2'].astype(str) + '<br>' + 'SO2: ' + \
                    df['SO2'].astype(str) + '<br>' + 'PM2.5: ' + df['PM2.5'].astype(str) + '<br>' + 'PM10: ' + \
                    df['PM10'].astype(str) + '<br>' + 'OX: ' + df['OX'].astype(str)

px.set_mapbox_access_token("pk.eyJ1IjoibWF0dGhld3AxMzEiLCJhIjoiY2xybHJvbDZ0MHBlMjJrcXdpZjk1aWNwbSJ9.MzuOnvZ25yb2upVacPwyEw")
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
                        hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
                        color="total_score", zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'])
# fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# fig = go.Figure()
#
# fig.add_trace(go.Scattergeo(
#     locationmode = 'ISO-3',
#     lon = df['longitude'],
#     lat = df['latitude'],
#     text = df['text'],
#     marker = dict(
#         color = df['total_score'],
#         line_color='rgb(40,40,40)',
#         line_width=0.5,
#     ),
#     name = df['measurement_station_code'].to_string()))
#
# fig.update_layout(
#     title_text = 'Japan - 2021 Average Air Quality (NMHC, SO2, NO2, PM2.5, PM10, OX)',
#     geo = dict(
#         scope = 'asia',
#         landcolor = 'rgb(217, 217, 217)',
#     )
# )
#
# fig.show()