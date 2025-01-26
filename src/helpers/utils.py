from dotenv import dotenv_values
import os
from typing import Optional, List, Dict
from pathlib import Path
import pandas as pd
import glob


def get_files_paths(main_folder, dataset_name, extension):
    """
    Searches for all files with the specified extension in the given folder and subfolders
    that start with the specified dataset name.

    Args:
        main_folder (str): Path to the main folder to search within.
        dataset_name (str): Prefix of the file names to search for.
        extension (str): File extension to search for (e.g., 'csv', 'xlsx').

    Returns:
        list: List of file paths that match the criteria.
    """
    pattern = os.path.join(main_folder, "**", f"{dataset_name}*.{extension}")
    file_list = glob.glob(pattern, recursive=True)
    return file_list


def load_files(file_paths):
    """
    Reads multiple files based on their extension and combines them into a single DataFrame.

    Args:
        file_paths (list): List of file paths to be loaded.

    Returns:
        pd.DataFrame: Combined DataFrame containing data from all files.
    """
    dataframes = []

    for path in file_paths:
        extension = os.path.splitext(path)[-1].lower()
        if extension == ".csv":
            df = read_csv(path)
        elif extension == ".xlsx":
            df = read_excel(path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")

        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df


def check_file_exists(file_path, error_message=None):
    """
    Check if a file exists at the specified path.

    Args:
        file_path (str): The path of the file to check.
        error_message (str, optional): A custom error message if the file does not exist.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(error_message or f"File does not exist: {file_path}")


def check_folder_exists(folder_path, error_message=None):
    """
    Check if a folder exists at the specified path.

    Args:
        folder_path (str): The path of the folder to check.
        error_message (str, optional): A custom error message if the folder does not exist.

    Raises:
        FileNotFoundError: If the folder does not exist.
    """
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(
            error_message or f"Folder does not exist: {folder_path}"
        )


def create_folder(folder_path):
    """
    Create a folder if it does not exist.

    Args:
        folder_path (str): The path of the folder to create.

    Raises:
        OSError: If the folder cannot be created.
    """
    if not os.path.isdir(folder_path):
        print(f"Folder does not exist. Creating folder: {folder_path}")
        os.makedirs(folder_path, exist_ok=True)
        if os.path.isdir(folder_path):
            print(f"Folder {folder_path} was successfully created.")
        else:
            raise OSError(f"Failed to create folder: {folder_path}")
    else:
        print(f"Folder {folder_path} already exists.")


def read_csv(file_path, **kwargs):
    """
    Read a CSV file and return its content as a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        **kwargs: Additional arguments to pass to pandas.read_csv.

    Returns:
        pd.DataFrame: The contents of the CSV file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be read.
    """
    check_file_exists(file_path, f"CSV file not found: {file_path}")
    try:
        return pd.read_csv(file_path, **kwargs)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {file_path}\nError: {e}")


def write_csv(data, file_path, **kwargs):
    """
    Write a pandas DataFrame to a CSV file with customizable options.

    Args:
        data (pd.DataFrame): The data frame to be written to the CSV file.
        file_path (str): The path to save the CSV file.
        **kwargs: Additional arguments to pass to pandas.DataFrame.to_csv.

    Raises:
        ValueError: If the file cannot be written.
    """
    try:
        data.to_csv(file_path, **kwargs)
        print(f"CSV file successfully written to: {file_path}")
    except Exception as e:
        raise ValueError(f"Failed to write CSV file: {file_path}\nError: {e}")


def filter_dataframe(df, filter_dict):
    """
    Filters the DataFrame based on conditions specified in a dictionary.

    Args:
        df (pd.DataFrame): The DataFrame to be filtered.
        filter_dict (dict): Dictionary with column names as keys and filter values as values.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    for key, value in filter_dict.items():
        df = df[df[key] == value]
    return df


def analyze_dataframe(dataframe):
    """
    Analyzes DataFrame columns by calculating missing data statistics, unique value counts, and data types.

    Args:
        dataframe (pd.DataFrame): Input DataFrame for analysis.

    Returns:
        pd.DataFrame: Analysis results with columns:
            - column_name: Name of each column
            - missing_values_total: Count of missing values
            - missing_values_percent: Percentage of missing values
            - unique_values_count: Count of unique values
            - data_type: Data type of each column
    """
    results = []

    for col in dataframe.columns:
        missing_total = dataframe[col].isnull().sum()
        missing_percent = 100 * missing_total / len(dataframe)

        unique_count = dataframe[col].nunique()
        data_type = dataframe[col].dtype

        results.append([col, missing_total, missing_percent, unique_count, data_type])

    analysis_df = pd.DataFrame(
        results,
        columns=[
            "column_name",
            "missing_values_total",
            "missing_values_percent",
            "unique_values_count",
            "data_type",
        ],
    )

    return analysis_df


def fill_missing_values_based_on_column_mapping(
    df, target_col="Województwo", reference_col="Nazwa świadczeniodawcy"
):
    """
    Fills missing values in the target column based on unique values from the reference column.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        target_col (str): The column in which missing values will be filled.
        reference_col (str): The column used to map values to the target column.

    Returns:
        pd.DataFrame: DataFrame with filled missing values.
    """
    unique_reference_df = (
        df[[target_col, reference_col]].dropna().drop_duplicates(keep="first")
    )

    # Check for duplicates in the reference column
    duplicate_reference_df = unique_reference_df[
        unique_reference_df[reference_col].duplicated(keep=False)
    ]
    duplicate_reference_values = set(duplicate_reference_df[reference_col])

    # Identify rows where target column is missing and reference column is not null
    missing_target_condition = df[target_col].isna() & df[reference_col].notna()

    # Filter rows where reference column value is not duplicated
    filtered_df = df[
        missing_target_condition & ~df[reference_col].isin(duplicate_reference_values)
    ]

    # Create mapping dictionary
    reference_to_target_mapping = dict(
        zip(unique_reference_df[reference_col], unique_reference_df[target_col])
    )

    # Fill missing values using the mapping
    df.loc[filtered_df.index, target_col] = df.loc[
        filtered_df.index, reference_col
    ].map(reference_to_target_mapping)

    return df


def read_excel(file_path, **kwargs):
    """
    Read an Excel file and return its content as a pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.
        **kwargs: Additional arguments to pass to pandas.read_excel.

    Returns:
        pd.DataFrame: The contents of the Excel file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be read.
    """
    # Check if the file exists
    check_file_exists(file_path, f"Excel file not found: {file_path}")

    # Try reading the Excel file
    try:
        return pd.read_excel(file_path, **kwargs)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {file_path}\nError: {e}")


def write_excel(file_path: str, data: pd.DataFrame, **kwargs):
    """
    Write a pandas DataFrame to an Excel file. Allows overwriting the file or appending to it.

    Args:
        file_path (str): The path to the Excel file.
        data (pd.DataFrame): The DataFrame to write to the file.
        **kwargs: Additional arguments for pandas Excel writer and `DataFrame.to_excel`.
            - mode (str): Writing mode ('w' to overwrite the file or 'a' to append). Defaults to 'w'.
            - engine (str): Engine to use for writing. Defaults to 'openpyxl'.
            - if_sheet_exists (str): Action if the sheet exists ('error', 'replace', or 'new'). Defaults to 'replace'.
            - sheet_name (str): The name of the sheet to write to. Defaults to 'Sheet1'.
            - Additional arguments supported by pandas `DataFrame.to_excel`.

    Raises:
        ValueError: If the writing mode or other parameters are invalid.
    """
    try:
        # Extract optional arguments with defaults
        mode = kwargs.pop("mode", "w")
        engine = kwargs.pop("engine", "openpyxl")

        # Handle if_sheet_exists only for append mode
        if mode == "a":
            if_sheet_exists = kwargs.pop("if_sheet_exists", "replace")
            with pd.ExcelWriter(
                file_path, mode=mode, engine=engine, if_sheet_exists=if_sheet_exists
            ) as writer:
                data.to_excel(writer, **kwargs)
        elif mode == "w":
            # Write mode (overwrite file entirely)
            with pd.ExcelWriter(file_path, mode=mode, engine=engine) as writer:
                data.to_excel(writer, **kwargs)
        else:
            raise ValueError("Invalid mode. Use 'w' for overwrite or 'a' for append.")

    except Exception as e:
        raise ValueError(f"Failed to write to Excel file: {file_path}. Error: {e}")


def left_join_excel_sheets(file_path, base_df=None, on=None, **kwargs):
    """
    Iteratively left joins all sheets of an Excel file to a base DataFrame.

    Args:
        file_path (str): Path to the Excel file.
        base_df (pd.DataFrame or None): The base DataFrame to join with. If None, starts with the first sheet.
        on (list or str): Column(s) to join on. Passed to pd.merge.
        **kwargs: Additional arguments for read_excel.

    Returns:
        pd.DataFrame: A single DataFrame after left joining all sheets.
    """
    # Load the Excel file and get all sheet names
    try:
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {file_path}. Error: {e}")

    # Initialize base_df if not provided
    if base_df is None:
        try:
            base_df = read_excel(file_path, sheet_name=sheet_names[0], **kwargs)
            sheet_names = sheet_names[1:]  # Remove the first sheet from processing
        except Exception as e:
            raise ValueError(f"Error processing sheet {sheet_names[0]}: {e}")

    # Iteratively join each sheet
    for sheet in sheet_names:
        try:
            # Read the current sheet
            sheet_df = read_excel(file_path, sheet_name=sheet, **kwargs)

            # Perform a left join with the base DataFrame
            base_df = base_df.merge(sheet_df, how="left", on=on)

        except Exception as e:
            print(f"Error processing sheet {sheet}: {e}")

    return base_df


def aggregate_count(df, group_columns=None, value_columns=None, header="Count"):
    """
    Aggregates and counts occurrences in a DataFrame grouped by specified columns.
    Creates a hierarchical structure with `group_columns` and `value_columns`.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to aggregate.
    - group_columns (list): List of column names to group by.
    - value_columns (list or None): List of column names whose unique values become new columns.
    - header (str): Header for the resulting count column.

    Returns:
    - pd.DataFrame: A DataFrame with hierarchical structure and counts.
    """
    # Validate input
    if group_columns is None or not group_columns:
        raise ValueError("group_columns cannot be None or empty.")

    # Initialize results
    results = []

    # Process each group column
    for group_col in group_columns:
        if value_columns is None:
            # Count unique occurrences in the group column
            counts = df[group_col].value_counts().reset_index()
            counts.columns = ["Value", header]
            counts["Column"] = group_col
            counts.set_index(["Column", "Value"], inplace=True)
            results.append(counts)
        else:
            # Group by group_col and value_columns
            grouped = (
                df.groupby([group_col] + value_columns).size().reset_index(name=header)
            )

            # Pivot value_columns into separate columns
            pivot_table = grouped.pivot(
                index=group_col, columns=value_columns[0], values=header
            ).fillna(0)

            # Reset index and include group_col as part of hierarchical index
            pivot_table["Column"] = group_col
            pivot_table.reset_index(inplace=True)
            pivot_table.set_index(["Column", group_col], inplace=True)

            results.append(pivot_table)

    # Combine results into a single DataFrame
    combined_results = pd.concat(results, axis=0)

    # Ensure proper column names and indices
    if value_columns is not None:
        combined_results.columns.name = None  # Remove column name for value_columns
    return combined_results


def aggregate_sum(df, group_columns=None, value_columns=None, header=None):
    """
    Aggregates a DataFrame using the 'sum' function.
    Creates a hierarchical index for `group_columns` and aggregates numerical `value_columns`.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to aggregate.
    - group_columns (list): List of column names to group by and create hierarchical index.
    - value_columns (list): List of numerical column names to aggregate.
    - header (str or None): Prefix for the resulting aggregation columns. If None, no prefix is added.

    Returns:
    - pd.DataFrame: A DataFrame with hierarchical index and aggregated columns.
    """
    # Validate input
    if group_columns is None or not group_columns:
        raise ValueError("group_columns cannot be None or empty.")
    if value_columns is None or not value_columns:
        raise ValueError("value_columns cannot be None or empty.")

    # Check if value_columns are numeric
    for col in value_columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must be numeric for sum aggregation.")

    # Initialize results
    results = []

    # Process each group column
    for group_col in group_columns:
        # Group by the group column and aggregate the value columns
        grouped = df.groupby(group_col)[value_columns].sum().reset_index()

        # Add "Column" level to the index for hierarchical structure
        grouped["Column"] = group_col
        grouped.set_index(["Column", group_col], inplace=True)

        # Optionally rename the columns with the header prefix
        if header:
            grouped.columns = [f"{header}_{col}" for col in grouped.columns]

        results.append(grouped)

    # Concatenate results for all group_columns
    result_df = pd.concat(results)

    return result_df
