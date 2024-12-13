# Recovery Score Calculations: Identification of Regions of Interest helper
# Script created  3/25/2024
# Last revision 12/13/2024

import numpy as np
import pandas as pd
from numpy.typing import NDArray

def set_jerk_threshold(jerk: NDArray[np.float64], factor: float, percentile: float) -> tuple:
    '''Sets the jerk threshold based on the mean and standard deviation of the jerk values

    Args:
    jerk (NDArray[np.float64]): Array of jerk values
    factor (float): Multiplication factor for the standard deviation
    percentile (int): Percentile value to use for setting the threshold

    Returns:
        tuple: The calculated jerk threshold
    '''
    mean_jerk = np.mean(jerk)
    std_jerk = np.std(jerk)
    percentile_jerk = np.percentile(jerk, percentile)
    jerk_threshold_cal = max(mean_jerk + factor * std_jerk, percentile_jerk)
   
    return mean_jerk, std_jerk, jerk_threshold_cal

def calculate_window_sd(df, window_size, step_size)-> list:
    ''' Creates a window to scan the data. The window size is 'window_size' data points and the window is advancing every 'step_size' datapoints.
        Function calculates the standard deviation (SD) over a specified window size with a specified step size

    Args:
        df: jerk data. First derivative of acceleration data on Z axis (Acc_Z)
        window_size: window size
        step_size: number of data points by which the window advances

    Returns:
        list of float values
    '''
    
    print('calculating window_sd...')

    n: int = len(df)
    sd_list: list = []
    for i in range(0, n - window_size + 1, step_size):
        window = df[i : i + window_size]
        sd = np.std(window)
        sd_list.append(sd)
    
    return sd_list

def detect_roi_sd(AccZ_sd: list, threshold: float) -> list:
    '''Identifies Regions of Interest in the data based on a threshold criterion 
        applied to the standard deviation values (AccZ_sd)
        It filters out regions where the standard deviation is greater than or equal to twice 
        the threshold value (threshold). These regions are stored in the filtered list along with their indexes.

    Args:
        AccZ_sd: list with the all the regions that have a standad deviation greater or equal to twice the threshold
        threshold: threshold value for standard deviation
        
    Returns:
        list with the regions of interest
    '''

    filtered = list()
    
    for i in range(len(AccZ_sd)):
        if AccZ_sd[i] > threshold*2:
            filtered.append((i, AccZ_sd[i]))

    regions_of_interest = list()
    big = 0
    index = 0
    for j in range(len(filtered) - 1):
        if filtered[j][0] + 1 == filtered[j + 1][0]:
            if filtered[j][1] > big:
                big = filtered[j][1]
                index = filtered[j][0]
            elif filtered[j + 1][1] > big:
                big = filtered[j + 1][1]
                index = filtered[j + 1][0]
        elif big > 0:
            regions_of_interest.append((index, big))
            big = 0
            index = 0
        
    regions_of_interest.append((index, big))
    
    return regions_of_interest

def get_attempts_sd(regions_of_interest: list) ->int:
    ''' Counts the number of identified regions of interest. Since the last region will always be
        the successful attempt, it substracts 1 to the final count

    Args:
        regions_of_interest: list with the all the regions that have a standad deviation > set threshold

    Returns:
        int with Number of failed Attempts
    '''

    attempts: int = len(regions_of_interest) - 1

    return attempts

def get_roi_indices(jerk: NDArray[np.float64], snap: NDArray[np.float64], jerk_threshold_cal: float, snap_threshold: float) -> pd.DataFrame:
    '''Identifies indices of regions of interest (ROIs) where jerk, snap or jerk or snap exceed specified thresholds.

    Args:
        jerk (NDArray[np.float64]): Array of jerk values
        snap (NDArray[np.float64]): Array of snap values
        jerk_threshold_cal (float): Threshold for jerk values
        snap_threshold (float): Threshold for snap values

    Returns:
       Pandas DataFrame: Indices of regions of interest
    '''
    # Ensure both arrays have the same length
    min_length = min(len(jerk), len(snap))
    jerk = jerk[:min_length]
    snap = snap[:min_length]
       
    # Detect ROIs where either jerk or snap exceed thresholds
    roi_mask = (np.abs(jerk) > jerk_threshold_cal) | (np.abs(snap) > snap_threshold)
    roi_indices = np.where(roi_mask)[0]  # Get indices of true values in the mask

    # Convert to pandas DataFrame
    roi_indices_df = pd.DataFrame(roi_indices, columns=['ROI_Indices'])

    return roi_indices_df
 
def get_attempts(roi_indices_df) -> int:
    ''' Counts the number of identified regions of interest. Since the last region will always be
        the successful attempt, it substracts 1 to the final count

    Args:
        roi_indices: list with the all the regions that have a jerk > set threshold

    Returns:
        int with Number of failed Attempts
    '''

    number_failed_attempts: int = len(roi_indices_df) - 1

    return number_failed_attempts


def get_roi_derivative(jerk, snap, jerk_threshold_cal, snap_threshold) -> list:
    ''' Identifies Regions of Interest in the data based on a threshold criterion 
        applied to the Jerk and Snap values
        It filters out regions where the Jerk and Snap are greater than or equal to the threshold value.
        These regions are stored in the filtered list along with their indexes.

    Args:
        jerk: list with the all the regions that have a jerk greater or equal to the threshold
        snap: list with the all the regions that have a snap greater or equal to the threshold
        jerk_threshold_cal: threshold value for Jerk after re calibration
        snap_threshold: threshold value for Snap
        
    Returns:
        list with the regions of interest for Jerk and Snap
    '''
    filtered = list()
    for i in range(len(jerk)):
        if jerk[i] > jerk_threshold_cal:
            filtered.append((i, jerk[i]))
    
    for i in range(len(snap)):
        if snap[i] > snap_threshold:
            filtered.append((i, snap[i]))

    roi_derivative = list() #
    big = 0
    index = 0
    for j in range(len(filtered) - 1):
        if filtered[j][0] + 1 == filtered[j + 1][0]:
            if filtered[j][1] > big:
                big = filtered[j][1]
                index = filtered[j][0]
            elif filtered[j + 1][1] > big:
                big = filtered[j + 1][1]
                index = filtered[j + 1][0]
        elif big > 0:
            roi_derivative.append((index, big))
            big = 0
            index = 0
        
    roi_derivative.append((index, big))
    
    return roi_derivative
