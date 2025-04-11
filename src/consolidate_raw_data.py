import argparse
import os
import os.path
import re

import pandas


def extract_pollutant_id_from_filename(filename):
    """
    Extracts the two-digit pollutant code from a filename matching the
    pattern TD<year><month><day/seq>.txt using regex.

    Args:
        filename (str): The filename to process (can include path).

    Returns:
        str: The extracted two-digit month number as a string, or None if the
             pattern is not found.
    """
    # Regex pattern:
    # TM      - Matches the literal characters "TM"
    # \d{4}   - Matches exactly four digits (the year)
    # (\d{2}) - Matches exactly two digits (the month) and captures them (group 1)
    # \d{2}   - Matches exactly two digits (likely day or sequence)
    # \.txt   - Matches the literal ".txt" extension
    # Use os.path.basename to ensure we only match against the filename part
    basename = os.path.basename(filename)
    pattern = r"TD\d{4}(\d{2})\d{2}\.txt"
    match = re.search(pattern, basename)

    if match:
        # The captured month is in group 1
        return int(match.group(1))

    return None


def get_all_files(directory_path):
    """
    Returns a list of fully qualified paths for all files in the given directory
    and its subdirectories.

    Args:
        directory_path (str): The path to the directory (can be relative or absolute).

    Returns:
        list: A list of fully qualified (absolute) file paths.
    """
    file_paths = []
    # os.walk works correctly with relative paths.
    # We will make the output paths absolute.
    for root, _, files in os.walk(directory_path):
        for filename in files:
            # Construct the full path by joining the root directory and filename
            filepath = os.path.join(root, filename)
            # Ensure the path is absolute
            absolute_filepath = os.path.abspath(filepath)
            file_paths.append(absolute_filepath)

    # Check if the directory exists implicitly by seeing if os.walk yielded anything
    if not file_paths and not os.path.isdir(directory_path):
        print(
            f"Warning: Directory not found or is empty at {os.path.abspath(directory_path)}"
        )

    return file_paths


def keep_cols_up_to_substring(df, substring):
    """
    Keeps all columns in a DataFrame from the beginning up to and including
    the first column whose name contains the given substring.

    Args:
        df (pd.DataFrame): The input DataFrame.
        substring (str): The substring to search for in column names.

    Returns:
        pd.DataFrame: A DataFrame containing the selected columns. If no column
                      name contains the substring, the original DataFrame is returned.
    """
    all_columns = df.columns.tolist()
    target_index = -1

    # Find the index of the first column containing the substring
    for i, col_name in enumerate(all_columns):
        if substring in col_name:
            target_index = i
            break  # Stop after finding the first match

    if target_index != -1:
        # Select columns from the start up to and including the target index
        # .iloc is efficient for integer-based indexing
        return df.iloc[:, : target_index + 1]

    # If no column contains the substring, return the original DataFrame
    print(
        f"Warning: No column name containing '{substring}' found. Returning original DataFrame."
    )
    return df


def add_percentage_score_column(df, substring):
    """
    Finds the first column in a DataFrame whose name contains a given substring,
    then adds a new 'Score' column representing each value in the target column
    as a percentage of its maximum value.

    Args:
        df (pd.DataFrame): The input DataFrame.
        substring (str): The substring to search for in column names.

    Returns:
        pd.DataFrame: The DataFrame with the added 'Score' column, or the
                      original DataFrame if no matching column is found or if
                      the target column is unsuitable for calculation.
    """
    target_col_name = None
    # Find the first column containing the substring
    for col_name in df.columns:
        if substring in col_name:
            target_col_name = col_name
            break  # Stop after finding the first match

    if target_col_name is None:
        print(
            f"Warning: No column name containing '{substring}' found. No 'Score' column added."
        )
        return df

    # Check if the target column is numeric
    if not pandas.api.types.is_numeric_dtype(df[target_col_name]):
        print(
            f"Warning: Target column '{target_col_name}' is not numeric. Cannot calculate percentage score."
        )
        return df

    # Calculate the maximum value in the target column
    max_value = df[target_col_name].max()

    # Handle potential division by zero or max_value being NaN
    if pandas.isna(max_value):
        print(
            f"Warning: Maximum value in '{target_col_name}' is NaN. Cannot calculate percentage score."
        )
        return df

    if max_value == 0:
        print(
            f"Warning: Maximum value in '{target_col_name}' is 0. Setting all scores to 0."
        )
        df["Score"] = 0.0
    else:
        # Calculate the percentage score
        df["Score"] = df[target_col_name] / max_value

    return df


def remove_rows_by_values(df, column_name, values_to_remove):
    """
    Removes rows from a DataFrame where the value in the specified column
    is present in the provided list of numbers.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to check.
        values_to_remove (list): A list of numbers. Rows where the value
                                 in 'column_name' matches any number in
                                 this list will be removed.

    Returns:
        pd.DataFrame: A new DataFrame with the specified rows removed.
                      Returns the original DataFrame if the column doesn't exist.
    """
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        print(
            f"Warning: Column '{column_name}' not found in DataFrame. Returning original DataFrame."
        )
        return df

    # Create a boolean Series: True if the column value IS IN the list
    is_in_list = df[column_name].isin(values_to_remove)

    # Filter the DataFrame: Keep rows where the value IS NOT IN the list (invert the boolean Series)
    df_filtered = df[~is_in_list]

    return df_filtered


def main():
    """
    Take raw csv files of each pollutant and combine them in one XLSX with sheets named by pollutant
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "raw_data_dir",
        help="a directory of TDYYYYXX00.txt files with Shift-JIS CSV of pollutant data",
    )
    parser.add_argument(
        "output_xlsx",
        help="filename for XLSX output, same as file with stations output from address_to_gps.py",
    )
    args = parser.parse_args()

    pollutant_names = [
        None,
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
        "SP",
        "PM25",
    ]
    yearly_avg = "年平均値"
    station_code = "測定局コード"
    stations_to_ignore = [
        # Sakurajima Volcano (obviously not fair for comparing SO2 levels)
        46201220,
        # Kagoshima-ken, Kanoya-shi, just a little south of Sakurajima, and I can't imagine
        # it would actually have the highest annual PM2.5 in Japan apart from the 2022 eruption
        46203010,
    ]

    files = get_all_files(args.raw_data_dir)
    for file in files:
        pollutant_id = extract_pollutant_id_from_filename(file)

        # Skip other kinds of data files
        if pollutant_id is None:
            continue

        pollutant_name = pollutant_names[pollutant_id]

        df = pandas.read_csv(file, encoding="shift_jisx0213")

        # Remove problematic stations
        df = remove_rows_by_values(df, station_code, stations_to_ignore)

        # Trim off excess columns
        df = keep_cols_up_to_substring(df, yearly_avg)

        # Calculate percentile score
        df = add_percentage_score_column(df, yearly_avg)

        with pandas.ExcelWriter(
                args.output_xlsx, if_sheet_exists="overlay", mode="a"
        ) as excel_writer:
            df.to_excel(excel_writer, sheet_name=pollutant_name, index=False)

        print(f"Wrote {pollutant_name}")


if __name__ == "__main__":
    main()
