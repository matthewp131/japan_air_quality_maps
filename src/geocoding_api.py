import os
from dotenv import load_dotenv

import googlemaps
import json
import pandas
import argparse

def main():
    """
    Call Google Geocoding API on monitoring station addresses and produce a JSON file with the API responses
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="a XLSX Workbook with a Stations sheet produced by address_to_gps.py")
    parser.add_argument("input_sheet", help="sheet name inside XLSX file, probably Stations")
    parser.add_argument("gps_json", help="filename for JSON output of GPS info")
    args = parser.parse_args()

    station_code = "国環研局番"

    load_dotenv()
    gmaps = googlemaps.Client(key=os.getenv('GEOCODING_API_KEY'))

    with open(args.input_file, 'rb') as f:
        df = pandas.read_excel(f, sheet_name=[args.input_sheet])[args.input_sheet]

    output = []

    for index, row in df.iterrows():
        print(row[station_code])
        geocode_result = gmaps.geocode(row["full_address"])
        output.append({"station_code": row[station_code], "full_address": row["full_address"], "response": geocode_result[0]})

    with open(args.gps_json, "w", encoding="utf-16") as outfile:
        json.dump(output, outfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()