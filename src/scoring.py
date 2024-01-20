import pandas
import openpyxl

with open('../data/2021_with_scoring.xlsx', 'rb') as f:
    all_pollutants = pandas.read_excel(f, sheet_name=['NMHC','SO2','NO2','PM2.5','PM10','OX', 'Stations'])

msc = '測定局コード'
prefecture_romaji = '都道府県名_ローマ字'
city_romaji = '市区町村名_ローマ字'
station_name = '測定局名'
station_code = "国環研局番"
nmhc = all_pollutants['NMHC']
so2 = all_pollutants['SO2']
no2 = all_pollutants['NO2']
pm25 = all_pollutants['PM2.5']
pm10 = all_pollutants['PM10']
ox = all_pollutants['OX']
stations = all_pollutants['Stations']

aq_scores = {}

for index, row in nmhc.iterrows():
    aq_score_dict = {'measurement_station_code': row[msc],
                     'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                     'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                     'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                      'NMHC': row['Score'],
                     'SO2': None,
                     'NO2': None,
                     'PM2.5': None,
                     'PM10': None,
                     'OX': None,
                     'total_score': None
                      }
    aq_scores[row[msc]] = aq_score_dict

for index, row in so2.iterrows():
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['SO2'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                     'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                     'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                      'NMHC': None,
                     'SO2': row['Score'],
                     'NO2': None,
                     'PM2.5': None,
                     'PM10': None,
                     'OX': None,
                     'total_score': None
                      }
        aq_scores[row[msc]] = aq_score_dict

for index, row in no2.iterrows():
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['NO2'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                     'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                     'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                      'NMHC': None,
                     'SO2': None,
                     'NO2': row['Score'],
                     'PM2.5': None,
                     'PM10': None,
                     'OX': None,
                     'total_score': None
                      }
        aq_scores[row[msc]] = aq_score_dict

for index, row in pm25.iterrows():
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['PM2.5'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                     'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                     'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                      'NMHC': None,
                     'SO2': None,
                     'NO2': None,
                     'PM2.5': row['Score'],
                     'PM10': None,
                     'OX': None,
                     'total_score': None
                      }
        aq_scores[row[msc]] = aq_score_dict

for index, row in pm10.iterrows():
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['PM10'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                     'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                     'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                      'NMHC': None,
                     'SO2': None,
                     'NO2': None,
                     'PM2.5': None,
                     'PM10': row['Score'],
                     'OX': None,
                     'total_score': None
                      }
        aq_scores[row[msc]] = aq_score_dict

for index, row in ox.iterrows():
    if row[msc] in aq_scores:
        aq_scores[row[msc]]['OX'] = row['Score']
    else:
        aq_score_dict = {'measurement_station_code': row[msc],
                         'full_address': stations.loc[stations[station_code] == row[msc], "full_address"].item(),
                     'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                     'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                      'NMHC': None,
                     'SO2': None,
                     'NO2': None,
                     'PM2.5': None,
                     'PM10': None,
                     'OX': row['Score'],
                     'total_score': None
                      }
        aq_scores[row[msc]] = aq_score_dict

for msc_id, aq_score in aq_scores.items():
    num_measurements = 0
    total_score = 0
    if aq_score['NO2'] is not None and aq_score['PM2.5'] is not None and aq_score['PM10'] is not None:
        for k, v in aq_score.items():
            if k in ['NMHC', 'SO2', 'NO2', 'PM2.5', 'PM10', 'OX']:
                if v is not None:
                    total_score += v
                    num_measurements += 1
        total_score = total_score / num_measurements
        aq_score['total_score'] = total_score

df = pandas.DataFrame(aq_scores.values())
df = df.sort_values(by=['total_score'])

print(df.head())

df.to_excel('out.xlsx', index=False)
