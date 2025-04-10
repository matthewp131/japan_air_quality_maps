import plotly.express as px
import pandas as pd

px.set_mapbox_access_token("pk.eyJ1IjoibWF0dGhld3AxMzEiLCJhIjoiY2xybHJvbDZ0MHBlMjJrcXdpZjk1aWNwbSJ9.MzuOnvZ25yb2upVacPwyEw")

with open('../hk2022.xlsx', 'rb') as f:
    df = pd.read_excel(f, sheet_name=['scores'])['scores']

df['size'] = 0.1
# df['hover_data'] = '<br>NMHC: ' + df['NMHC'].astype(str) + '<br>' + 'NOX: ' + df['NOX'].astype(str) + '<br>' + 'SO2: ' + \
#                     df['SO2'].astype(str) + '<br>' + 'PM2.5: ' + df['PM2.5'].astype(str) + '<br>' + 'PM10: ' + \
#                     df['PM10'].astype(str) + '<br>' + 'OX: ' + df['OX'].astype(str)


main_pollutant = 'Month 02'
df1 = df.loc[df[main_pollutant].notna()]
fig = px.scatter_mapbox(df1, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="STATION",
                        # hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
                        color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
                        # color_continuous_midpoint=0.5,
                        title=main_pollutant)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


main_pollutant = 'AVG'
df2 = df.loc[df[main_pollutant].notna()]
fig = px.scatter_mapbox(df2, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="STATION",
                        # hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
                        color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
                        # color_continuous_midpoint=0.5,
                        title=main_pollutant)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
