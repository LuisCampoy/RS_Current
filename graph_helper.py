# Recovery Score Calculations: Graph_Helper Script
# Script created  3/25/2024
# Last revision 5/31/2025

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import config

from numpy.typing import NDArray

def plot_acceleration_data(df_filtered: pd.DataFrame, df_moving_avg: pd.DataFrame, df_butterworth: pd.DataFrame) -> None:
    '''
    Plots two graphs for df_filtered and df_moving_avg.

    Args:
        df_filtered (pd.DataFrame): DataFrame with filtered acceleration data.
        df_moving_avg (pd.DataFrame): DataFrame with moving average filtered acceleration data.
        df_butterworth (pd.DataFrame): DataFrame with Butterworth filtered acceleration data.
    Returns:
        None
    '''
    plt.figure(figsize=(15, 10))

    # Plot df_filtered
    plt.subplot(3, 1, 1)
    plt.plot(df_filtered['timeStamp'], df_filtered['Acc_X'], label='Acc_X', color='blue')
    plt.plot(df_filtered['timeStamp'], df_filtered['Acc_Y'], label='Acc_Y', color='green')
    plt.plot(df_filtered['timeStamp'], df_filtered['Acc_Z'], label='Acc_Z', color='red')
    plt.title('Filtered Acceleration Data')
    plt.xlabel('Time')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.grid(True)

    # Plot df_moving_avg
    plt.subplot(3, 1, 2)
    plt.plot(df_moving_avg['timeStamp'], df_moving_avg['Acc_X'], label='Acc_X', color='blue')
    plt.plot(df_moving_avg['timeStamp'], df_moving_avg['Acc_Y'], label='Acc_Y', color='green')
    plt.plot(df_moving_avg['timeStamp'], df_moving_avg['Acc_Z'], label='Acc_Z', color='red')
    plt.title('Moving Average Filtered Acceleration Data')
    plt.xlabel('Time')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.grid(True)

    # Plot df_butterworth
    plt.subplot(3,1,3)
    plt.plot(df_butterworth['timeStamp'], df_butterworth['Acc_X'], label='Acc_X', color='blue')
    plt.plot(df_butterworth['timeStamp'], df_butterworth['Acc_Y'], label='Acc_Y', color='green')
    plt.plot(df_butterworth['timeStamp'], df_butterworth['Acc_Z'], label='Acc_Z', color='red')
    plt.title('Butterworth Filtered Acceleration Data')
    plt.xlabel('Time')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def get_plot_jerk(jerk: np.ndarray, df: pd.DataFrame) -> None:
    '''
    Plots jerk

    Args:
        jerk (np.ndarray): The first derivative of acceleration (jerk)
        jerk_butterworth (np.ndarray): The first derivative of acceleration (jerk) after Butterworth filtering
        df: provides TimeStamp list for the X axis
    '''
    time_stamp_np: NDArray = np.array(df['timeStamp'], dtype=np.float64)
     # Adjust timeStamp to match the length of jerk
    timeStamp_jerk = time_stamp_np[:-1]
    
    # Plot size
    plt.figure(figsize=(12, 6))
    
    # Jerk plot
    plt.plot(timeStamp_jerk, jerk, label="Jerk", color="blue")
    
    # Convert timestamps to numerical values
    #timeStamp_jerk_num = mdates.date2num(timeStamp_jerk)
    # Highlight ROIs
    #for i in roi_indices['ROI_Indices']:
    #   plt.axvspan(float(timeStamp_jerk_num[i] - 0.5), float(timeStamp_jerk_num[i] + 0.5), color='grey', alpha=0.3, label="ROI" if i == roi_indices[0] else "")
        
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Jerk")
    plt.xlabel("Time")
    plt.ylabel("Jerk")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.tight_layout()
    plt.show()

def get_plot_jerk_with_roi(jerk:np.ndarray, df:pd.DataFrame, roi_sd:list, window_size:int, step_size:int, file_path:str) -> None:
    '''
    Creates a plot of the Z axis only with the detected Regions of Interest
    
    Args:
        jerk: np.ndarray with the jerk values
        df: pd.DataFrame with the timeStamp and Acc_Z values
        roi_sd: list with the regions of interest detected
        window_size: int with the size of the window
        step_size: int with the step size
        file_path: string with the name of the file

    Returns:
        None
    '''
    time_stamp_np: NDArray = np.array(df['timeStamp'])
    # Adjust timeStamp to match the length of jerk and snap
    timeStamp_jerk = time_stamp_np[:-1]
    #timeStamp_snap = time_stamp_np[:-2]

    plt.figure(figsize=(10, 6))
    
    plt.plot(timeStamp_jerk, jerk, label="Jerk", color="blue")
    
    for k in range(len(roi_sd)):
        # Vertical lines for the start of the regions of interest
        plt.vlines(
            timeStamp_jerk[roi_sd[k][0] * step_size],
            config.YMIN,
            config.YMAX,
            colors= ['red'],
            linestyles= 'dashed',
            label= 'ROI',
        )
        # Vertical lines for the end of the regions of interest
        plt.vlines(
            df['timeStamp'][roi_sd[k][0] * step_size + window_size],
            config.YMIN,
            config.YMAX,
            colors= ['red'],
            linestyles= 'dashed',
        )
    plt.xlabel('timeStamp')
    plt.ylabel('jerk')
    plt.title(file_path)
    plt.grid(which='both')
    plt.legend()
    plt.show()

def plot_accel_data_with_roi_and_maxaccel(df: pd.DataFrame, roi_indexes: list, amax_x: list, amax_y: list, amax_z: list) -> None:
    '''
    Plots the acceleration data with ROI as Vlines and maximum accelerations in each ROI highlighted as dots.

    Args:
        roi_indexes (list[list[int]]): List of lists of indices for each ROI.
        amax_x_list (list[float]): List of maximum accelerations in X axis.
        amax_y_list (list[float]): List of maximum accelerations in Y axis.
        amax_z_list (list[float]): List of maximum accelerations in Z axis.
    Returns:
        None
    '''
    plt.figure(figsize=(15, 10))
    # Plot AccX, AccY, and AccZ
    plt.plot(df['timeStamp'], df['Acc_X'], label='Acc_X', color='blue')
    plt.plot(df['timeStamp'], df['Acc_Y'], label='Acc_Y', color='green')
    plt.plot(df['timeStamp'], df['Acc_Z'], label='Acc_Z', color='red')

    # Plot ROIs
    for i in range(len(roi_indexes)):
        indices = roi_indexes[i]
        if indices:  # check if not empty
            plt.axvspan(df['timeStamp'].iloc[indices].min(), df['timeStamp'].iloc[indices].max(), color='grey', alpha=0.5)

    # Plot maximum accelerations
    for i in range(len(roi_indexes)):
        indices = roi_indexes[i]
        if indices:
            plt.scatter(df['timeStamp'].iloc[indices], [amax_x[i]]*len(indices), color='blue', label='Max Acc_X' if i == 0 else "")
            plt.scatter(df['timeStamp'].iloc[indices], [amax_y[i]]*len(indices), color='green', label='Max Acc_Y' if i == 0 else "")
            plt.scatter(df['timeStamp'].iloc[indices], [amax_z[i]]*len(indices), color='red', label='Max Acc_Z' if i == 0 else "")

    plt.title('Filtered Acceleration Data with ROIs')
    plt.xlabel('Time')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.grid(True)
    plt.show()

"""
def get_plot_jerk_snap_with_roi(jerk: np.ndarray, snap: np.ndarray, roi_indices_df: pd.DataFrame, df_avg: pd.DataFrame) -> None:
    '''
    Plots jerk and snap, highlighting regions of interest (ROIs).

    Args:
        jerk (np.ndarray): The first derivative of acceleration (jerk).
        snap (np.ndarray): The second derivative of acceleration (snap).
        roi_indices_df: pd.DataFrame Indices of regions of interest.
        df_avd: pd.DataFrame: Time array corresponding to jerk and snap.
    '''
    time_stamp_np: NDArray = np.array(df_avg['timeStamp'], dtype=np.float64)
     # Adjust timeStamp to match the length of jerk and snap
    timeStamp_jerk = time_stamp_np[:-1]
    timeStamp_snap = time_stamp_np[:-2]
    
    # Plot jerk
    plt.figure(figsize=(12, 6))
    
    # Jerk plot
    plt.subplot(2, 1, 1)
    plt.plot(timeStamp_jerk, jerk, label="Jerk", color="blue")
    plt.scatter(timeStamp_jerk[roi_indices_df], jerk[roi_indices_df], color="red", label="ROI", zorder=5)
    
    # Convert timestamps to numerical values
    #timeStamp_jerk_num = mdates.date2num(timeStamp_jerk)
    # Highlight ROIs
    #for i in roi_indices['ROI_Indices']:
    #   plt.axvspan(float(timeStamp_jerk_num[i] - 0.5), float(timeStamp_jerk_num[i] + 0.5), color='grey', alpha=0.3, label="ROI" if i == roi_indices[0] else "")
        
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Jerk with Highlighted ROIs")
    plt.xlabel("Time")
    plt.ylabel("Jerk")
    plt.legend()
    plt.grid(True)

    # Snap plot
    plt.subplot(2, 1, 2)
    plt.plot(timeStamp_snap, snap, label="Snap", color="blue")
    #plt.scatter(timeStamp_snap[roi_indices], snap[roi_indices], color="red", label="ROI", zorder=5)
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Snap with Highlighted ROIs")
    plt.xlabel("Time")
    plt.ylabel("Snap")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.tight_layout()
    plt.show()
"""