import argparse
import pandas
import os.path

def main():
    """
    Convert a txt file in Shift-JIS CSV format of Japanese air quality monitoring stations
    into a sheet in an excel workbook with a `full_address` column properly formatted
    for use in the Google Geocoding API (see geocoding_api.py)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="a TMYYYY0000.txt file with Shift-JIS CSV of measuring station addresses")
    parser.add_argument("output_file", help="filename for XLSX output")
    parser.add_argument("output_sheet", help="sheet name inside XLSX file")
    args = parser.parse_args()

    headers = {
        "prefecture": "都道府県名",
        "city": "市区町村名",
        "address": "住所"
    }

    df = pandas.read_csv(args.input_file, encoding="shift_jisx0213")

    df["full_address"] = df[headers["prefecture"]].astype(str) + df[headers["city"]].astype(str) + df[headers["address"]].astype(str)

    # Reorder columns for convenience
    cols = list(df.columns)
    cols = cols[0:2] + [cols[-1]] + cols[2:-1]
    df = df[cols]

    print(df["full_address"].head())

    if os.path.isfile(args.output_file):
        with pandas.ExcelWriter(args.output_file, if_sheet_exists="overlay", mode="a") as excel_writer:
            df.to_excel(excel_writer, sheet_name=args.output_sheet, index=False)
    else:
        with pandas.ExcelWriter(args.output_file, mode="w") as excel_writer:
            df.to_excel(excel_writer, sheet_name=args.output_sheet, index=False)


if __name__ == "__main__":
    main()
