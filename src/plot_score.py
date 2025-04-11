import openpyxl
import plotly
import plotly.express as px
import pandas as pd

px.set_mapbox_access_token("pk.eyJ1IjoibWF0dGhld3AxMzEiLCJhIjoiY2xybHJvbDZ0MHBlMjJrcXdpZjk1aWNwbSJ9.MzuOnvZ25yb2upVacPwyEw")

with open('../output/2021_scores.xlsx', 'rb') as f:
    df = pd.read_excel(f)

df['size'] = 0.1
df['hover_data'] = '<br>NMHC: ' + df['NMHC'].astype(str) + '<br>' + 'NOX: ' + df['NOX'].astype(str) + '<br>' + 'SO2: ' + \
                    df['SO2'].astype(str) + '<br>' + 'PM2.5: ' + df['PM2.5'].astype(str) + '<br>' + 'PM10: ' + \
                    df['PM10'].astype(str) + '<br>' + 'OX: ' + df['OX'].astype(str)


# main_pollutant = '2PM2.5_PM10_NOX_SO2_NMHC_OX'
# df1 = df.loc[df[main_pollutant].notna()]
# fig = px.scatter_mapbox(df1, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
#                         hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
#                         color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
#                         # color_continuous_midpoint=0.5,
#                         title=main_pollutant)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


# main_pollutant = '2PM2.5_PM10_NOX_SO2_NMHC'
# df2 = df.loc[df[main_pollutant].notna()]
# fig = px.scatter_mapbox(df2, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
#                         hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
#                         color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
#                         # color_continuous_midpoint=0.5,
#                         title=main_pollutant)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


# main_pollutant = '2PM2.5_PM10_NOX_SO2'
# df3 = df.loc[df[main_pollutant].notna()]
# fig = px.scatter_mapbox(df3, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
#                         hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
#                         color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
#                         # color_continuous_midpoint=0.5,
#                         title=main_pollutant)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


# main_pollutant = '2PM2.5_PM10'
# df4 = df.loc[df[main_pollutant].notna()]
# fig = px.scatter_mapbox(df4, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
#                         hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
#                         color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
#                         # color_continuous_midpoint=0.5,
#                         title=main_pollutant)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

# main_pollutant = 'NMHC'
# df5 = df.loc[df[main_pollutant].notna()]
# fig = px.scatter_mapbox(df5, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
#                         hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
#                         color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
#                         # color_continuous_midpoint=0.5,
#                         title=main_pollutant)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()
#
# main_pollutant = 'NOX_SO2_NMHC'
# df5 = df.loc[df[main_pollutant].notna()]
# fig = px.scatter_mapbox(df5, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
#                         hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
#                         color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
#                         # color_continuous_midpoint=0.5,
#                         title=main_pollutant)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

main_pollutant = 'PM2.5'
df5 = df.loc[df[main_pollutant].notna()]
fig = px.scatter_mapbox(df5, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
                        hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
                        color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
                        # color_continuous_midpoint=0.5,
                        title=main_pollutant)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()
plotly.offline.plot(fig, filename='../output/japan_2021_pm2_5.html')

# main_pollutant = 'PM2.5_OX'
# df5 = df.loc[df[main_pollutant].notna()]
# fig = px.scatter_mapbox(df5, lat="latitude", lon="longitude", size="size", size_max=8, hover_name="full_address",
#                         hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
#                         color=main_pollutant, zoom=5, color_continuous_scale=['#0704c7','#6ff542','#fcfc0a','#f01616'],
#                         # color_continuous_midpoint=0.5,
#                         title=main_pollutant)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()