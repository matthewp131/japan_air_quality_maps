import argparse

import pandas
from pandas import Series


def get_value_and_suffix_from_substring(row: Series, substring):
    """
    Finds a column containing the substring, returns its value with the
    cleaned suffix of the column name.
    """

    for col_name in row.index.values:
        if substring in col_name:
            # Remove substring, strip whitespace, remove parentheses
            index = col_name.index(substring)
            start_index = index + len(substring)
            suffix = (
                col_name[start_index:]
                .strip()
                .replace("(", "")
                .replace(")", "")
            )
            return str(row[col_name]) + f" {suffix}"
    # Return None if no matching column is found
    return None


def main():
    """
    Look at the Score column from sheets for each pollutant in a workbook. Output a new workbook with all pollutant scores by column
    for each station.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_xlsx",
        help="a XLSX Workbook with individual sheets for each pollutant with a Score column, as well as Stations",
    )
    parser.add_argument(
        "output_xlsx",
        help="a XLSX Workbook storing scores by pollutant for each station",
    )
    args = parser.parse_args()

    msc = "測定局コード"
    station_code = "国環研局番"
    yearly_avg = "年平均値"

    with open(args.input_xlsx, "rb") as f:
        all_pollutants = pandas.read_excel(
            f,
            sheet_name=[
                "SO2",
                "NO",
                "NO2",
                "NOX",
                "CO",
                "OX",
                "NMHC",
                "CH4",
                "THC",
                "SPM",
                "PM25",
                "Stations",
            ],
        )

    pollutants_to_score = [
        "SO2",
        "NO",
        "NO2",
        "NOX",
        "CO",
        "OX",
        "NMHC",
        "CH4",
        "THC",
        "SPM",
        "PM25",
    ]
    stations = all_pollutants["Stations"]

    aq_scores = {}

    # Write individual pollutant scores
    for pollutant in pollutants_to_score:
        # Save a list of all the other pollutants in case we need to create a new row with empty columns
        other_pollutants = pollutants_to_score.copy()
        other_pollutants.remove(pollutant)

        # For every measurement station, copy score for each pollutant
        for _, row in all_pollutants[pollutant].iterrows():
            # Skip if we are missing Station info with GPS
            if stations.loc[stations[station_code] == row[msc]].empty:
                print("Station", row[msc], "not found")
                continue

            # also store raw values
            raw_col_name = pollutant + "_raw"
            raw_col_value = get_value_and_suffix_from_substring(row, yearly_avg)

            # If row for this measurement station already exists, add the score for this pollutant
            if row[msc] in aq_scores:
                aq_scores[row[msc]][pollutant] = row["Score"]
                aq_scores[row[msc]][raw_col_name] = raw_col_value
            # If need to add a new row, copy in Station info, and set other pollutant scores to None
            else:
                aq_score_dict = {
                    "measurement_station_code": row[msc],
                    "full_address": stations.loc[
                        stations[station_code] == row[msc], "full_address"
                    ].item(),
                    "latitude": stations.loc[
                        stations[station_code] == row[msc], "latitude"
                    ].item(),
                    "longitude": stations.loc[
                        stations[station_code] == row[msc], "longitude"
                    ].item(),
                    pollutant: row["Score"],
                    raw_col_name: raw_col_value,
                }
                for other_pollutant in other_pollutants:
                    aq_score_dict[other_pollutant] = None
                    aq_score_dict[other_pollutant + "_raw"] = None

                print(aq_score_dict)
                # Write new row
                aq_scores[row[msc]] = aq_score_dict

    # Calculate more composite air quality scores
    df = pandas.DataFrame(aq_scores.values())
    df["2PM2.5_OX_PM10_NOX_SO2_NMHC"] = None
    df["2PM2.5_OX_PM10_NOX_SO2"] = None
    df["2PM2.5_OX_PM10"] = None
    df["NOX_SO2_NMHC"] = None
    df["NOX_SO2"] = None

    # (2 * PM2.5 * OX) + PM10 + NOX + SO2 + NMHC
    df.loc[
        df["PM25"].notna()
        & df["OX"].notna()
        & df["SPM"].notna()
        & df["NOX"].notna()
        & df["SO2"].notna()
        & df["NMHC"].notna(),
        "2PM2.5_OX_PM10_NOX_SO2_NMHC",
    ] = (
        (df["PM25"] * df["OX"] * 2) + df["SPM"] + df["NOX"] + df["SO2"] + df["NMHC"]
    ) / 7

    # (2 * PM2.5 * OX) + PM10 + NOX + SO2
    df.loc[
        df["PM25"].notna()
        & df["OX"].notna()
        & df["SPM"].notna()
        & df["NOX"].notna()
        & df["SO2"].notna(),
        "2PM2.5_OX_PM10_NOX_SO2",
    ] = ((df["PM25"] * df["OX"] * 2) + df["SPM"] + df["NOX"] + df["SO2"]) / 6

    # (2 * PM2.5 * OX) + PM10
    df.loc[
        df["PM25"].notna() & df["OX"].notna() & df["SPM"].notna(), "2PM2.5_OX_PM10"
    ] = ((df["PM25"] * df["OX"] * 2) + df["SPM"]) / 3

    # NOX + SO2 + NMHC
    df.loc[
        df["NOX"].notna() & df["SO2"].notna() & df["NMHC"].notna(), "NOX_SO2_NMHC"
    ] = (df["NOX"] + df["SO2"] + df["NMHC"]) / 3

    # NOX + SO2
    df.loc[df["NOX"].notna() & df["SO2"].notna(), "NOX_SO2"] = (
        df["NOX"] + df["SO2"]
    ) / 2

    print(df.head())

    df.to_excel(args.output_xlsx, index=False)


if __name__ == "__main__":
    main()
