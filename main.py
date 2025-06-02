# RS: Main Script
# Script created 3/25/2024
# Last revision 5/31/2025
# Notes: this script uses the SD method to detect regions of interest using the jerk signal.
# once identified, it extracts the indexes of the regions of interest (ROIs) from the jerk signal.
# It then calculates the maximum accelerations for each axis (Acc_X, Acc_Y, Acc_Z) within those ROIs 
# # using the original, unfiltered signal
# Sensitivity variables in cofig file

import pandas as pd
import numpy as np

import config

from acceleration_helper import get_max_accelerations, get_sa_2axes, get_sumua
from attempt_detection_helper import calculate_window_sd, detect_roi_sd, get_attempts, get_indexes, set_jerk_threshold
from derivative_helper import calculate_derivatives
from file_helper import read_csv_file, initial_filter, apply_moving_average, apply_butterworth_filter
from graph_helper import plot_acceleration_data, get_plot_jerk, get_plot_jerk_with_roi, plot_accel_data_with_roi_and_maxaccel
from numpy.typing import NDArray
from region_helper import extract_accel_values_from_roi
from output_results_helper import process_recovery

def main() -> None:

    file_path: str = input('Enter case number: ')

    df: pd.DataFrame = read_csv_file(file_path)

    if df is not None:
        print('File read successfully...')
        print("Columns in DataFrame:", df.columns)
        
    else:
        print('Failed to load DataFrame')
        return # exit if the file cannot be loaded
    
    # Creates new df in which values are ignored until values in the Z-axis reach 'target_value' 
    # signaling horse getting onto sternal recumbency
    df_filtered: pd.DataFrame = initial_filter(df, config.TARGET_VALUE)
    print('Initial filter applied successfully')
       
    # Apply moving average filter with a specified 'target_moving_avg' value
    df_moving_avg: pd.DataFrame = apply_moving_average(df_filtered, config.TARGET_MOVING_AVG)
    print('Moving average applied successfully')

    df_butterworth: pd.DataFrame = apply_butterworth_filter(df_filtered, config.BUTTERWORTH_ORDER, config.BUTTERWORTH_CUTOFF, config.FS)
    print('Butterworth filter applied successfully')

    # Plot data to review application of filters
    plot_acceleration_data(df_filtered, df_moving_avg, df_butterworth)
          
    # Create new DataFrame after applying avg filter with Acc_Z and timeStamp values only 
    df_avg = pd.DataFrame({'timeStamp': df_moving_avg['timeStamp'], 'Acc_Z': df_moving_avg['Acc_Z']})
    
    # Create new DataFrame after applying Butterworth filter with Acc_Z and timeStamp values only
    df_butterworth = pd.DataFrame({'timeStamp': df_butterworth['timeStamp'], 'Acc_Z': df_butterworth['Acc_Z']})

    # Calculates first derivative (jerk) from the filtered dataset
    jerk: NDArray[np.float64] = calculate_derivatives(df_butterworth)
    print('First derivative calculated successfully')

    get_plot_jerk(jerk, df_butterworth)          
    
    # Set Jerk threshold and calculate mean Jerk to be able to re calibrate the threshold
    mean_jerk, std_jerk, jerk_threshold_cal = set_jerk_threshold(jerk, config.FACTOR, config.PERCENTILE)
    print('Jerk mean, SD and threshold calculated successfully')
    #print(f'Mean Jerk = {mean_jerk}')
    #print(f'Jerk threshold set to {jerk_threshold_cal}')
    
    print('Calculating ROIs on the jerk signal...')

    # Calculates standard deviation for each window
    AccZ_sd: list[float] = calculate_window_sd(jerk, config.WINDOW_SIZE, config.STEP_SIZE)
    print('sd_list calculated succesfully using jerk dataset')

    # Detects regions of interest on the jerk signal based on standard deviation method
    roi_sd: list[float] = detect_roi_sd(AccZ_sd, jerk_threshold_cal)
    print('Regions of Interest detected successfully')
    print(f'len(roi_sd): {len(roi_sd)}')
    print(roi_sd)

    # Alternatively, the get_roi_indexes function can be used to get the indexes of the regions of interest
   
    # Plot jerk with regions of interest using sd method
    get_plot_jerk_with_roi(jerk, df_butterworth, roi_sd, config.WINDOW_SIZE, config.STEP_SIZE, file_path)

    # Calculate Number of failed attempts        
    number_failed_attempts: int = get_attempts(roi_sd)
    print(f'Number of Failed Attempts = {number_failed_attempts}')

    # Extract list with indexes of the regions of interest using the jerk signal
    roi_indexes: list[list[int]] = get_indexes(roi_sd, config. WINDOW_SIZE, config.STEP_SIZE)
    print('indexes of the regions of interest extracted successfully')
    print(f'roi_indexes: {roi_indexes}')

    # Apply indexes to original dataset to obtain the actual acceleration values within each of the ROIs
    extracted_roi: list[pd.DataFrame] = extract_accel_values_from_roi(df_filtered, roi_indexes)
    print('ROI values extracted successfully')
    
    # Calculate max accelerations for each axis (AccX, AccY, AccZ) for each attempt
    # and store them in lists
    amax_x_list, amax_y_list, amax_z_list = get_max_accelerations(extracted_roi)
    print('Max accelerations calculated successfully')

    # Plot df with ROIs
    plot_accel_data_with_roi_and_maxaccel(df_filtered, roi_indexes, amax_x_list, amax_y_list, amax_z_list)
    #plot_accel_data_with_max_accel(df_filtered, extracted_roi, amax_x_list, amax_y_list, amax_z_list)

    sa_2axes: float = get_sa_2axes(amax_x_list, amax_y_list)
    #print(f'sa_2axes = {sa_2axes}')
                
    sumua:float = get_sumua(amax_x_list, amax_y_list, amax_z_list)
    #print(f'ua_list = {ua_list}')
    #print(f'sumua = {sumua}')
            
    rs_2axes_py: float = process_recovery(file_path, config.JERK_THRESHOLD, mean_jerk, std_jerk, jerk_threshold_cal, number_failed_attempts, sa_2axes, sumua)

    # display output_results in terminal
    print(f'results are:')
    print(f'file name: {file_path}')
    print(f'jerk_threshold: {config.JERK_THRESHOLD}')
    print(f'mean_jerk: {mean_jerk}')
    print(f'std_jerk:{std_jerk}')
    print(f'jerk_threshold_cal: {jerk_threshold_cal}')
    #print(f'threshold set at: {config.THRESHOLD}')
    print(f'len(roi_sd): {len(roi_sd)}')
    print(f'Number of failed attempts: {number_failed_attempts}')
    print(f'sa_2axes= {sa_2axes}')
    print(f'sumua= {sumua}')
    print(f'rs_2axes_py= {rs_2axes_py}')
 
if __name__ == "__main__":
    
    main()