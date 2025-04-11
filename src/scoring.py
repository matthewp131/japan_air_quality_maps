import pandas
import openpyxl
import argparse


def main():
    """
    Look at the Score column from sheets for each pollutant in a workbook. Output a new workbook with all pollutant scores by column
    for each station.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_xlsx",
                        help="a XLSX Workbook with individual sheets for each pollutant with a Score column, as well as Stations")
    parser.add_argument("output_xlsx", help="a XLSX Workbook storing scores by pollutant for each station")
    args = parser.parse_args()

    msc = '測定局コード'
    prefecture_romaji = '都道府県名_ローマ字'
    city_romaji = '市区町村名_ローマ字'
    station_name = '測定局名'
    station_code = "国環研局番"

    with open(args.input_xlsx, 'rb') as f:
        all_pollutants = pandas.read_excel(f, sheet_name=['NMHC', 'SO2', 'NOX', 'PM2.5', 'PM10', 'OX', 'Stations'])

    pollutants_to_score = ['NMHC', 'SO2', 'NOX', 'PM2.5', 'PM10', 'OX']
    stations = all_pollutants['Stations']

    aq_scores = {}

    # Write individual pollutant scores
    for pollutant in pollutants_to_score:
        # Save a list of all the other pollutants in case we need to create a new row with empty columns
        other_pollutants = pollutants_to_score.copy()
        other_pollutants.remove(pollutant)

        # For every measurement station, copy score for each pollutant
        for index, row in all_pollutants[pollutant].iterrows():
            # Skip if we are missing Station info with GPS
            if stations.loc[stations[station_code] == row[msc]].empty:
                print("Station", row[msc], "not found")
                continue

            # If row for this measurement station already exists, add the score for this pollutant
            if row[msc] in aq_scores:
                aq_scores[row[msc]][pollutant] = row['Score']
            # If need to add a new row, copy in Station info, and set other pollutant scores to None
            else:
                aq_score_dict = {
                    'measurement_station_code': row[msc],
                    'full_address': stations.loc[
                        stations[station_code] == row[msc], "full_address"].item(),
                    'latitude': stations.loc[stations[station_code] == row[msc], "latitude"].item(),
                    'longitude': stations.loc[stations[station_code] == row[msc], "longitude"].item(),
                    pollutant: row['Score'],
                }
                for other_pollutant in other_pollutants:
                    aq_score_dict[other_pollutant] = None

                # Write new row
                aq_scores[row[msc]] = aq_score_dict

    # Calculate more composite air quality scores
    df = pandas.DataFrame(aq_scores.values())
    df['2PM2.5_OX_PM10_NOX_SO2_NMHC'] = None
    df['2PM2.5_OX_PM10'] = None
    df['NOX_SO2_NMHC'] = None

    # (2 * PM2.5 * OX) + PM10 + NOX + SO2 + NMHC
    df.loc[df['PM2.5'].notna() & df['OX'].notna() & df['PM10'].notna() & df['NOX'].notna() & df['SO2'].notna() & df[
        'NMHC'].notna(), '2PM2.5_OX_PM10_NOX_SO2_NMHC'] = ((df['PM2.5'] * df['OX'] * 2) + df['PM10'] + df['NOX'] + df[
        'SO2'] + df['NMHC']) / 7

    # (2 * PM2.5 * OX) + PM10
    df.loc[df['PM2.5'].notna() & df['OX'].notna() & df['PM10'].notna(), '2PM2.5_OX_PM10'] = ((df['PM2.5'] * df[
        'OX'] * 2) + df['PM10']) / 3

    # NOX + SO2 + NMHC
    df.loc[df['NOX'].notna() & df['SO2'].notna() & df['NMHC'].notna(), 'NOX_SO2_NMHC'] = (df['NOX'] + df['SO2'] + df[
        'NMHC']) / 3

    print(df.head())

    df.to_excel(args.output_xlsx, index=False)


if __name__ == "__main__":
    main()
