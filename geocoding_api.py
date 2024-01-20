import googlemaps
import json
import pandas

station_code = "国環研局番"

def main():
    gmaps = googlemaps.Client(key='AIzaSyDiYs8zSK-R43YvIk19YeeHo6QbtK8xOY4')

    with open('2021_with_scoring.xlsx', 'rb') as f:
        df = pandas.read_excel(f, sheet_name=["Stations"])["Stations"]

    output = []

    for index, row in df.iterrows():
        print(row[station_code])
        geocode_result = gmaps.geocode(row["full_address"])
        output.append({"station_code": row[station_code], "full_address": row["full_address"], "response": geocode_result[0]})

    with open("gps.json", "w", encoding="utf-16") as outfile:
        json.dump(output, outfile, ensure_ascii=False, indent=2)

    with pandas.ExcelWriter(args.output_file, if_sheet_exists="overlay", mode="a") as excel_writer:
        df.to_excel(excel_writer, sheet_name="Stations", index=False)

if __name__ == "__main__":
    main()