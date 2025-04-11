# Plotly Mapping of Japan Air Quality Data

## View Air Quality Maps

See the [Github Pages](https://matthewp131.github.io/japan_air_quality_maps/) for this repo for the final output of
Japan Air Quality
maps, rendered with Plotly and displayed with Mapbox.

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