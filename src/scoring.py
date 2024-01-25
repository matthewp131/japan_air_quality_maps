import pandas
import openpyxl

with open('../data/2019_with_scoring.xlsx', 'rb') as f:
    all_pollutants = pandas.read_excel(f, sheet_name=['NMHC', 'SO2', 'NOX', 'PM2.5', 'PM10', 'OX', 'Stations'])

msc = '測定局コード'
prefecture_romaji = '都道府県名_ローマ字'
city_romaji = '市区町村名_ローマ字'
station_name = '測定局名'
station_code = "国環研局番"
nmhc = all_pollutants['NMHC']
so2 = all_pollutants['SO2']
nox = all_pollutants['NOX']
pm25 = all_pollutants['PM2.5']
pm10 = all_pollutants['PM10']
ox = all_pollutants['OX']
stations = all_pollutants['Stations']

aq_scores = {}

for index, row in nmhc.iterrows():
    if stations.loc[stations[station_code] == row[msc]].empty:
        print("Station", row[msc], "not found")
        continue
    aq_score_dict = {'measurement_station_code': row[msc],
                     'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                     'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                     'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                     'NMHC': row['Score'],
                     'SO2': None,
                     'NOX': None,
                     'PM2.5': None,
                     'PM10': None,
                     'OX': None,
                     }
    aq_scores[row[msc]] = aq_score_dict

for index, row in so2.iterrows():
    if stations.loc[stations[station_code] == row[msc]].empty:
        print("Station", row[msc], "not found")
        continue
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['SO2'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                         'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                         'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                         'NMHC': None,
                         'SO2': row['Score'],
                         'NOX': None,
                         'PM2.5': None,
                         'PM10': None,
                         'OX': None,
                         }
        aq_scores[row[msc]] = aq_score_dict

for index, row in nox.iterrows():
    if stations.loc[stations[station_code] == row[msc]].empty:
        print("Station", row[msc], "not found")
        continue
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['NOX'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                         'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                         'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                         'NMHC': None,
                         'SO2': None,
                         'NOX': row['Score'],
                         'PM2.5': None,
                         'PM10': None,
                         'OX': None,
                         }
        aq_scores[row[msc]] = aq_score_dict

for index, row in pm25.iterrows():
    if stations.loc[stations[station_code] == row[msc]].empty:
        print("Station", row[msc], "not found")
        continue
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['PM2.5'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                         'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                         'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                         'NMHC': None,
                         'SO2': None,
                         'NOX': None,
                         'PM2.5': row['Score'],
                         'PM10': None,
                         'OX': None,
                         }
        aq_scores[row[msc]] = aq_score_dict

for index, row in pm10.iterrows():
    if stations.loc[stations[station_code] == row[msc]].empty:
        print("Station", row[msc], "not found")
        continue
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['PM10'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                         'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                         'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                         'NMHC': None,
                         'SO2': None,
                         'NOX': None,
                         'PM2.5': None,
                         'PM10': row['Score'],
                         'OX': None,
                         }
        aq_scores[row[msc]] = aq_score_dict

for index, row in ox.iterrows():
    if stations.loc[stations[station_code] == row[msc]].empty:
        print("Station", row[msc], "not found")
        continue
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['OX'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                         'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                         'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                         'NMHC': None,
                         'SO2': None,
                         'NOX': None,
                         'PM2.5': None,
                         'PM10': None,
                         'OX': row['Score'],
                         }
        aq_scores[row[msc]] = aq_score_dict

df = pandas.DataFrame(aq_scores.values())

df['2PM2.5_PM10_NOX_SO2_NMHC_OX'] = None
df['2PM2.5_PM10_NOX_SO2_NMHC'] = None
df['2PM2.5_PM10_NOX_SO2'] = None
df['2PM2.5_PM10'] = None
df['NOX_SO2_NMHC'] = None

df.loc[df['PM2.5'].notna() & df['PM10'].notna() & df['NOX'].notna() & df['SO2'].notna() & df['NMHC'].notna() & df[
    'OX'].notna(), '2PM2.5_PM10_NOX_SO2_NMHC_OX'] = ((df['PM2.5'] * 2) + df['PM10'] + df['NOX'] + df['SO2'] + df[
    'NMHC'] + df['OX']) / 7

df.loc[df['PM2.5'].notna() & df['PM10'].notna() & df['NOX'].notna() & df['SO2'].notna() & df[
    'NMHC'].notna(), '2PM2.5_PM10_NOX_SO2_NMHC'] = ((df['PM2.5'] * 2) + df['PM10'] + df['NOX'] + df['SO2'] + df[
    'NMHC']) / 6

df.loc[df['PM2.5'].notna() & df['PM10'].notna() & df['NOX'].notna() & df['SO2'].notna(), '2PM2.5_PM10_NOX_SO2'] =\
        ((df['PM2.5'] * 2) + df['PM10'] + df['NOX'] + df['SO2']) / 5

df.loc[df['PM2.5'].notna() & df['PM10'].notna(), '2PM2.5_PM10'] = ((df['PM2.5'] * 2) + df['PM10']) / 3

df.loc[df['NOX'].notna() & df['SO2'].notna() & df['NMHC'].notna(), 'NOX_SO2_NMHC'] =\
    (df['NOX'] + df['SO2'] + df['NMHC']) / 3

print(df.head())

df.to_excel('../output/2019_scores.xlsx', index=False)
