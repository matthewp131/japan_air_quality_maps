# Plotly Mapping of Japan Air Quality Data

## View Air Quality Maps

See the [Github Pages](https://matthewp131.github.io/japan_air_quality_maps/) for this repo for the final output of Japan Air Quality
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

WIP...see data already in `data` directory

### Run Python Scripts

#### Monitoring stations

Go to TBD and download station locations txt file. It is already included in `data/TM20210000.txt`.

```bash
cd src
python ./address_to_gps.py ../data/TM20210000.txt ../data/2021.xlsx Stations
```

#### Fetch GPS Location of all Stations

```bash
python ./geocoding_api.py ../data/2021.xlsx Stations ../output/gps_2021.json
```

#### Add GPS Lat/Lon to XLSX

```bash
python ./import_gps.py ../output/gps_2021.json ../data/2021.xlsx Stations
```

#### Produce Scoring Sheet

```bash
python .\scoring.py ..\data\2021.xlsx ../output/test.xlsx
```

#### Generate Plotly Maps

```bash
python .\plot_score.py ../output/2021_scores.xlsx ..\docs\plotly\
```