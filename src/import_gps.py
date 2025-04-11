import json
import pandas
import argparse

def main():
    """
    Extract Lat/Lon from geocoding API response data and add "latitude" and "longitude" columns to the Stations sheet
    in an excel workbook
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("gps_json", help="JSON GPS info")
    parser.add_argument("stations_xlsx", help="a XLSX Workbook with a Stations sheet produced by address_to_gps.py")
    parser.add_argument("input_sheet", help="sheet name inside XLSX file, probably Stations")
    args = parser.parse_args()

    station_code = "国環研局番"

    with open(args.gps_json, "r", encoding="utf-16") as gps_json:
        geocoding_results = json.load(gps_json)

    with open(args.stations_xlsx, 'rb') as f:
        df = pandas.read_excel(f, sheet_name=[args.input_sheet])[args.input_sheet]

    df[["latitude", "longitude"]] = None
    for geocoding_result in geocoding_results:
        df.loc[df[station_code] == geocoding_result["station_code"], "latitude"] = geocoding_result["response"]["geometry"]["location"]["lat"]
        df.loc[df[station_code] == geocoding_result["station_code"], "longitude"] = geocoding_result["response"]["geometry"]["location"]["lng"]

    print(df[[station_code, "latitude", "longitude"]].head())

    with pandas.ExcelWriter(args.stations_xlsx, if_sheet_exists="overlay", mode="a") as excel_writer:
        df.to_excel(excel_writer, sheet_name=args.input_sheet, index=False)


if __name__ == "__main__":
    main()