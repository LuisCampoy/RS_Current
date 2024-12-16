# RS: Main Script
# Script created 3/25/2024
# Last revision 12/13/2024
# Notes: Use SD method to detect regions of interest using the jerk/ snap signal. 
# Then it, uses those indexes on the original Acc_Z, Acc_X, Acc_Y dataset

import pandas as pd
import numpy as np

from acceleration_helper import get_max_accelerations_x, get_max_accelerations_y, get_max_accelerations_z, get_sa_2axes, get_sumua
from attempt_detection_helper import calculate_window_sd, detect_roi_sd, get_roi_derivative, get_roi_indices, get_attempts, set_jerk_threshold
from derivative_helper import calculate_derivatives
from file_helper import read_csv_file, add_csv_extension, initial_filter, apply_moving_average, clean_data, apply_kalman_filter
from graph_helper import plot_acceleration_data, get_plot_jerk_snap, get_plot_jerk_snap_with_roi, get_plot_sd_with_roi
from numpy.typing import NDArray
from region_helper import extract_roi_values, get_number_roi_sd
from output_results_helper import process_recovery
#from velocity_helper import get_auc_x, get_auc_y, get_auc_z

def main() -> None:

    # acceleration threshold value to signal sternal recumbency for initial filter
    target_value: float = 9.0 
    
    # variables for moving average filter
    target_moving_avg: int = 10 # moving average window_size (4)
    
    # variables for Kalman filter
    process_variance = 1e-5  # Q
    measurement_variance = 1e-1  # R
    estimated_measurement_variance = 1.0  # P   
    
    # variables for ROI_Derivative method
    factor: float = 8.0   # Factor to set jerk threshold (56.55)
    percentile: float = 95.0    # Percentile to set jerk threshold  
    jerk_threshold: float = 5.7209199129367875e-12  # Threshold for significant jerk
    snap_threshold: float = 1  # Threshold for significant snap

    # variables for ROI_SD method
    # values that can be changed  to increase/ decrease sensitivity
    window_size: int = 2500 # each cell is 5ms, 10000 cells represent 2secs
    step_size: int = 833 # 2000 cells are 400ms (0.4secs)
    threshold: float = 1e-08 # default value for SD threshold 1.5
    
    file_path: str = input('Enter case number: ')
        
    df: pd.DataFrame = read_csv_file(file_path)

    if df is not None:
        print('File read successfully...')
        print("Columns in DataFrame:", df.columns)
        
    else:
        print('Failed to load DataFrame')
        return # exit if the file cannot be loaded
    
    # Creates new df in which Z_axis values are ignored until values reach 'target_value' 
    # signaling horse getting onto sternal recumbency
    df_filtered: pd.DataFrame = initial_filter(df, target_value)
    print('Initial filter applied successfully')
       
    # Apply moving average filter with a specified 'target_moving_avg' value
    df_moving_avg: pd.DataFrame = apply_moving_average(df_filtered, target_moving_avg)
    print('Moving average applied successfully')
    
    #df_kalman: pd.DataFrame = apply_kalman_filter(df_filtered, process_variance, measurement_variance, estimated_measurement_variance)
    #print('Kalman filter applied successfully')
    
    # Plot data to review application of filters
    #plot_acceleration_data(df_filtered, df_moving_avg, df_kalman)
          
    # Creates new DataFrame after applying avg filter with Acc_Z and timeStamp values only 
    df_avg = pd.DataFrame({'timeStamp': df_moving_avg['timeStamp'], 'Acc_Z': df_moving_avg['Acc_Z']})
        
    # Creates new DataFrame with Acc_Z and timeStamp values only (Kalman filter applied)
    #df_kalman = pd.DataFrame({'Acc_Z': df_kalman['Acc_Z'], 'timeStamp': df_kalman['timeStamp']})   
        
    # Calculates first and second derivatives (jerk and snap) from the avg filtered dataset
    jerk, snap= calculate_derivatives(df_avg)
    print('Jerk and Snap calculated successfully')

    #get_plot_jerk_snap(jerk, snap, df_avg)          
    # Converts onto pandas DataFrame
    #jerkdf = pd.DataFrame({'TimeStamp':timeStamp_np,'Jerk':jerk})
    #print('Jerk DataFrame created successfully')
    #snapdf = pd.DataFrame(snap, columns=['TimeStamp','Jerk'])
    #print('Snap DataFrame created successfully')
    
    # Set Jerk threshold and calculate mean Jerk to be able to re calibrate the threshold
    mean_jerk, std_jerk, jerk_threshold_cal = set_jerk_threshold(jerk, factor, percentile)
    print('Jerk threshold calculated successfully')
    #print(f'Mean Jerk = {mean_jerk}')
    #print(f'Jerk threshold set to {jerk_threshold_cal}')
        
    # Get regions of interest for Jerk and Snap
    #roi_indices_df: list[float] = get_roi_derivative(jerk, snap, jerk_threshold_cal, snap_threshold)
    #print('ROI calculated successfully')
    #print(f'ROI Derivative {roi_derivative}')
    
    print('Calculating ROIs...')

    # Calculates standard deviation for each window
    AccZ_sd: list[float] = calculate_window_sd(jerk, window_size, step_size)
    print('sd_list calculated succesfully using jerk dataset')

    # Detects regions of interest on the jerk signal based on standard deviation method
    roi_sd: list[float] = detect_roi_sd(AccZ_sd, threshold)
    print('Regions of Interest detected successfully')  

    # Get indices of regions of interest for Jerk and Snap  
    #roi_indices_df: pd.DataFrame = get_roi_indices(jerk, snap, jerk_threshold_cal, snap_threshold)
    #print('ROI indices obtained successfully')
    #print(f'ROI indices {roi_indices_df}')
        
    # Plot jerk and snap with regions of interest
    #get_plot_jerk_snap_with_roi(jerk, snap, roi_in dices_df, df_avg)

    # Plot jerk and snap with regions of interest using sd method
    get_plot_sd_with_roi(jerk, df_avg, roi_sd, window_size, step_size, file_path)
            
    number_failed_attempts: int = get_attempts(roi_sd)
    print(f'Number of Failed Attempts = {number_failed_attempts}')
    
    # Extract ROI values for each axis
    axes: list[str] = ['Acc_Z', 'Acc_X', 'Acc_Y']
    #roi_values_df: pd.DataFrame = extract_roi_values(df_moving_avg, roi_indices_df, axes)
    #print('ROI values extracted successfully')
    #print(roi_values_df)
    #print(f'ROI_Values_length = {len(roi_values_df)}')
    
    #selected_data_list: list = get_roi_derivative(jerk, snap, jerk_threshold_cal, snap_threshold)
            
    #selected_data_list_jerk_method: list = get_regions_jerk(jerk, roi_indices)
    #selected_data_list_snap_method: list = get_regions_snap(snap, roi_indices)
    
    roi_values: list = get_number_roi_sd(df, roi_sd, window_size, step_size)
                            
    amax_x_list: list[float] = get_max_accelerations_x(roi_values)
    #print(f'amax_x_list is {amax_x_list}')
                    
    amax_y_list: list[float] = get_max_accelerations_y(roi_values)
    #print(f'amax_y_list is {amax_y_list}')
                
    amax_z_list: list[float] = get_max_accelerations_z(roi_values)
    #print(f'amax_z_list is {amax_z_list}')
                
    #sa: float = get_sa(amax_x_list, amax_y_list, amax_z_list)
    #print(f'sa = {sa}')

    sa_2axes: float = get_sa_2axes(amax_x_list, amax_y_list)
    #print(f'sa_2axes = {sa_2axes}')
                
    sumua:float = get_sumua(amax_x_list, amax_y_list, amax_z_list)
    #print(f'ua_list = {ua_list}')
    #print(f'sumua = {sumua}')
            
    rs_2axes_py: float = process_recovery(file_path, jerk_threshold, mean_jerk, std_jerk, jerk_threshold_cal, threshold, number_failed_attempts, sa_2axes, sumua)

    # display output_results in terminal
    print(f'results are:')
    print(f'file name: {file_path}')
    print(f'jerk_threshold: {jerk_threshold}')
    print(f'mean_jerk: {mean_jerk}')
    print(f'std_jerk:{std_jerk}')
    print(f'jerk_threshold_cal: {jerk_threshold_cal}')
    print(f'threshold set at: {threshold}')
    print(f'len(roi_sd): {len(roi_sd)}')
    print(f'Number of failed attempts: {number_failed_attempts}')
    print(f'sa_2axes= {sa_2axes}')
    print(f'sumua= {sumua}')
    print(f'rs_2axes_py= {rs_2axes_py}')
 
if __name__ == "__main__":
    
    main()