import openpyxl
import plotly
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
import os
import argparse
from pathlib import Path


def main():
    """
    Produce Plotly maps with dots colored according to air quality
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("scores_xlsx", help="a XLSX Workbook storing scores by pollutant for each station")
    parser.add_argument("output_dir", help="output directory for html maps")
    args = parser.parse_args()

    load_dotenv()

    px.set_mapbox_access_token(os.getenv('GH_PAGES_MAPBOX_API_TOKEN'))

    with open(args.scores_xlsx, 'rb') as f:
        df = pd.read_excel(f)

    df['size'] = 0.1
    df['hover_data'] = '<br>NMHC: ' + df['NMHC'].astype(str) + '<br>' + 'NOX: ' + df['NOX'].astype(
        str) + '<br>' + 'SO2: ' + \
                       df['SO2'].astype(str) + '<br>' + 'PM2.5: ' + df['PM2.5'].astype(str) + '<br>' + 'PM10: ' + \
                       df['PM10'].astype(str) + '<br>' + 'OX: ' + df['OX'].astype(str)

    pollutants_to_map = ['PM2.5', '2PM2.5_OX_PM10_NOX_SO2_NMHC', '2PM2.5_OX_PM10', 'NOX_SO2_NMHC']

    for pollutant in pollutants_to_map:
        df5 = df.loc[df[pollutant].notna()]
        fig = px.scatter_mapbox(df5, lat="latitude", lon="longitude", size="size", size_max=8,
                                hover_name="full_address",
                                hover_data={"hover_data": True, "size": False, "latitude": False, "longitude": False},
                                color=pollutant, zoom=5,
                                color_continuous_scale=['#0704c7', '#6ff542', '#fcfc0a', '#f01616'],
                                # color_continuous_midpoint=0.5,
                                title=pollutant)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        # fig.show()
        filename = os.path.join(args.output_dir,
                                Path(args.scores_xlsx).stem + '_' + pollutant.replace('.', '_') + '.html')
        plotly.offline.plot(fig, filename=filename)


if __name__ == "__main__":
    main()
