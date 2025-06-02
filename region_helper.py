# Recovery Score Calculations: Calculation helper
# Script created  3/25/2024
# Last revision 5/22/2025

import pandas as pd

def extract_accel_values_from_roi(df: pd.DataFrame, indexes: list[list[int]])-> list[pd.DataFrame]:
    ''' 
    Extracts a list of DataFrames containing the acceleration values (Acc_X, Acc_Y, Acc_Z) from each of the regions of interest.
    Each region starts at an index = indexes[i][0] and ends at an index = indexes[i][1].
    The function iterates through the list of indexes and extracts the corresponding acceleration values from the DataFrame.
    It creates a new DataFrame for each region of interest, containing the acceleration values for the specified axes (Acc_X, Acc_Y, Acc_Z).
    The extracted DataFrames are stored in a list and returned.

    Args:
        df (pd.DataFrame): DataFrame containing the regions of interest.
        indexes (list): List of indexes corresponding to the regions of interest.

    Returns:
        list [pd.DataFrame]: list of DataFrames with the extracted acceleration values.
    '''
    print('extracting roi values...')

    extracted_dfs = []
    for idx in indexes:
        if idx[0] in df.index and idx[1] in df.index:
            extracted_dfs.append(df.loc[idx[0]:idx[1], ['Acc_X', 'Acc_Y', 'Acc_Z']].copy())
        else:
            print(f"Warning: Index {idx} not found in DataFrame and will be skipped.")

    return extracted_dfs
