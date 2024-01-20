import json
import pandas

station_code = "国環研局番"

def main():
    with open("../output/gps.json", "r", encoding="utf-16") as infile:
        geocoding_results = json.load(infile)

    with open('../data/2021_with_scoring.xlsx', 'rb') as f:
        df = pandas.read_excel(f, sheet_name=['Stations'])['Stations']

    df[["latitude", "longitude"]] = None
    for geocoding_result in geocoding_results:
        df.loc[df[station_code] == geocoding_result["station_code"], "latitude"] = geocoding_result["response"]["geometry"]["location"]["lat"]
        df.loc[df[station_code] == geocoding_result["station_code"], "longitude"] = geocoding_result["response"]["geometry"]["location"]["lng"]

    print(df[[station_code, "latitude", "longitude"]].head())

    with pandas.ExcelWriter('../data/2021_with_scoring.xlsx', if_sheet_exists="overlay", mode="a") as excel_writer:
        df.to_excel(excel_writer, sheet_name="Stations", index=False)


if __name__ == "__main__":
    main()