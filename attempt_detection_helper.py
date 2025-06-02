# Recovery Score Calculations: Identification of Regions of Interest helper
# Script created  3/25/2024
# Last revision 5/22/2025

import numpy as np

def set_jerk_threshold(jerk, factor, percentile) -> tuple:
    '''
    Sets the jerk threshold based on the mean and standard deviation of the jerk values

    Args:
    jerk (NDArray[np.float64]): Array of jerk values
    factor (float): Multiplication factor for the standard deviation
    percentile (int): Percentile value to use for setting the threshold

    Returns:
        tuple: The calculated jerk threshold
    '''
    mean_jerk: float = np.mean(jerk)
    std_jerk = np.std(jerk)
    percentile_jerk = np.percentile(jerk, percentile)
    jerk_threshold_cal: float = max(mean_jerk + factor * std_jerk, percentile_jerk)
   
    return mean_jerk, std_jerk, jerk_threshold_cal

def calculate_window_sd(df, window_size, step_size)-> list:
    ''' 
    Creates a window to scan the data. The window size is 'window_size' data points and the window is advancing every 'step_size' datapoints.
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
    '''
    Identifies Regions of Interest (ROI) using the first derivative signal based on a threshold criterion
    applied to the standard deviation values (AccZ_sd)
    Returns a list of (index, SD) for all windows above threshold.
    Args
        AccZ_sd: list with the all the regions that have a standard deviation greater than the threshold
        threshold: results of set_threshold_cal function
    Returns:
        list with the regions of interest
    '''
    regions_of_interest = []
    for i, sd in enumerate(AccZ_sd):
        if sd > threshold:
            regions_of_interest.append((i, sd))
    return regions_of_interest

def get_attempts(roi) -> int:
    ''' 
    Counts the number of identified regions of interest. Since the last region will always be
    the successful attempt, it substracts 1 to the final count

    Args:
        roi: list with the all the regions that have a jerk > set threshold

    Returns:
        int with Number of failed Attempts
    '''

    number_failed_attempts: int = len(roi) - 1

    return number_failed_attempts

def get_indexes(roi: list, window: int, step) -> list[list[int]]:
    ''' 
    Creates a list of lists of indexes: one list per roi (len((roi)). 
    Each list will start with the index of the first element of roi_sd and will end with that index * step_size + window_size

    Args:
        df: list with the all the regions that have a jerk > set threshold

    Returns:
        list with the indexes of the regions of interest
    '''
    print('getting indexes...')
    indexes: list[list[int]] = []
    for i in range(len(roi)):
        start = roi[i][0] * step
        end = start + window
        indexes.append([start, end])

    return indexes