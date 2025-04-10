import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime

# Step 1: Fetch Weather Data from JMA API
# JMA API endpoint for observation data
# This is a hypothetical endpoint, you may need to adjust it based on actual JMA API documentation
jma_api_url = "https://api.jma.go.jp/v1/fetch/namedayall?areaName=%E6%97%A5%E6%9C%AC%E5%85%A8%E5%9C%B0"

# Fetch weather data from JMA
def fetch_jma_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from JMA: {response.status_code}")

# Process JMA data to extract humidity and other relevant information
def process_jma_data(data):
    records = []
    for record in data['area']['city']:
        city = record['name']
        for day in record['timeseries'][0]['data']:
            date = day['date']
            for observation in day['observation']:
                if '湿度' in observation:
                    humidity = observation['湿度']['value']
                    records.append({
                        'city': city,
                        'date': date,
                        'humidity': humidity
                    })
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    return df

# Fetch and process JMA data
jma_data = fetch_jma_data(jma_api_url)
weather_data = process_jma_data(jma_data)

# Calculate average humidity by city and month
average_humidity = weather_data.groupby(['city', 'month'])['humidity'].mean().reset_index()

# Step 2: Fetch City Coordinates using OpenCage API
# OpenCage API endpoint
opencage_api_url = "https://api.opencagedata.com/geocode/v1/json"

# OpenCage API key (replace with your actual API key)
opencage_api_key = "6f879f0265f44b6b89ab81c4ce5f7f71"

# Fetch coordinates for each city
def fetch_coordinates(city, api_url, api_key):
    params = {
        'q': city + ", Japan",
        'key': api_key
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            result = data['results'][0]
            return result['geometry']['lat'], result['geometry']['lng']
    return None, None

# List of unique cities from weather data
cities = weather_data['city'].unique()

# Fetch coordinates for each city
coordinates = {}
for city in cities:
    lat, lon = fetch_coordinates(city, opencage_api_url, opencage_api_key)
    if lat and lon:
        coordinates[city] = {'latitude': lat, 'longitude': lon}

# Convert coordinates to DataFrame
city_coordinates = pd.DataFrame(list(coordinates.items()), columns=['city', 'coords'])
city_coordinates[['latitude', 'longitude']] = pd.DataFrame(city_coordinates['coords'].tolist(), index=city_coordinates.index)
city_coordinates.drop(columns=['coords'], inplace=True)

# Step 3: Combine Humidity Data with Coordinates
# Merge average humidity data with city coordinates
merged_data = pd.merge(average_humidity, city_coordinates, on='city')

# Step 4: Plot Data using Plotly
# Plot using Plotly
fig = px.scatter_geo(
    merged_data,
    lat='latitude',
    lon='longitude',
    hover_name='city',
    hover_data=['humidity'],
    color='humidity',
    color_continuous_scale=px.colors.sequential.Viridis,
    title='Average Relative Humidity by City in Japan',
    projection='natural earth'
)

# Update layout
fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular',
        center=dict(lon=138, lat=36),
        scope='asia'
    )
)

# Show the plot
fig.show()

# Optionally, save the plot
pio.write_image(fig, 'japan_humidity_map.png')