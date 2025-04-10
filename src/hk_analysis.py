import pandas as pd

df = pd.read_csv("hk2022.csv")
# df = df.groupby(by=["YEAR", "STATION"])
# df.index = pd.MultiIndex.from_arrays(df[['STATION', 'POLLUTANT']].values.T, names=['idx1', 'idx2'])
# df.set_index(['STATION'])
# df['Score'] = 10

print(df.head(10))
# print(df.transpose().head(10))
# for row in df.iterrows():
#     print(row)
# print(df.groupby(by="STATION").head())

stations = df['STATION'].unique()
dfs_by_station = {}
for station in stations:
    dfs_by_station[station] = df.loc[df['STATION'] == station].transpose()
    
for s in dfs_by_station.values():
    s['Score'] = (s['Fine Suspended Particulates'] * 2 + s['Nitrogen Oxides'] + s['Ozone'] + s['Respirable Suspended Particulates'] + s['Sulphur Dioxide']) / 6
    print(s.head())
