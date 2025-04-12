# Plotly Mapping of Japan Air Quality Data

## View Air Quality Maps

See the [Github Pages](https://matthewp131.github.io/japan_air_quality_maps/) for this repo for the final output of
Japan Air Quality
maps, rendered with Plotly and displayed with Mapbox.

## Methodology

This collection of scripts combines the Japan NIES Air Quality data files into a single XLSX spreadsheet, enriches the
measurement station data with GPS Lat/Lon locations using the Google Geocoding API, and scores each pollutant as a
proportion of the max for that pollutant. For example, measurement station 3320520 with address 岡山県笠岡市茂平２８０ is
located at (34.4942919, 133.4605572) and has an annual average PM2.5 of 14.3 μg/m3, which is the highest in Japan so it
receives a score of 1. Measurement station 1202080 with address 北海道函館市北美原１−９−１６ is located at (36.1461065,
137.2522083) and has an annual average PM2.5 of 4.4 μg/m3, which is the lowest in Japan, so it receives a score of
0.3077.

These scores are plotted using Plotly on top of a Mapbox map. As the most generally accepted guage of pollution, the
PM2.5 map shows that, in addition to urban areas being worse than rural ones, air quality is generally worse going
towards the south and west. In addition to single pollutant scores, I have selected a few combinational equations for
aggregating scores of multiple pollutants. For combined scores, only measurement stations which contained all of the
pollutants in the equation are included. This means that the combined maps sometimes have significantly fewer
measurement locations. The `(2 * PM2.5 * OX) + PM10 + NOX + SO2` appears to give the best overall impression of air
pollution, with Osaka standing out as having 11 of the highest scores in the top 25.

## Run it locally

### Dependencies

In addition to dependencies specified by import statements, you will also need to install openpyxl.

### Environment Variables

Obtain a [Geocoding API](https://developers.google.com/maps/documentation/geocoding) Key and a [Mapbox API]() Token.

Create a .env file as follows:

```bash
GEOCODING_API_KEY=<YOUR_KEY>
GH_PAGES_MAPBOX_API_TOKEN=<YOUR_KEY>
```

### Download Data and Calculate Scores Column

[National Institute for Environmental Studies, The Environmental Observatory, Air Pollution Monitoring Data File](https://tenbou.nies.go.jp/download/)

* 測定局データ for Monitoring Station data
* 月間値・年間値データ for Air Quality data

See data already in `data` directory

### Run Python Scripts

#### Monitoring stations

```bash
cd src
python ./address_to_gps.py ../data/2022_raw/TM20220000.txt ../data/2022.xlsx Stations
```

#### Calculate Scores for each Pollutant

```bash
python .\consolidate_raw_data.py ../data/2022_raw ../data/2022.xlsx
```

#### Fetch GPS Location of all Stations

```bash
python ./geocoding_api.py ../data/2022.xlsx Stations ../output/gps_2022.json
```

#### Add GPS Lat/Lon to XLSX

```bash
python ./import_gps.py ../output/gps_2022.json ../data/2022.xlsx Stations
```

#### Produce Scoring Sheet

```bash
python .\scoring.py ..\data\2022.xlsx ../output/2022_scores.xlsx
```

#### Generate Plotly Maps

```bash
python .\plot_score.py ../output/2022_scores.xlsx ..\docs\plotly\
```