# Config script
# This script contains the configuration settings for the analysis of accelerometer data.
# Script created on 5/19/2025
# Last revision: 5/26/2025

# acceleration threshold value to signal sternal recumbency for initial filter
TARGET_VALUE: float = 9.0 
    
# variables for moving average filter
TARGET_MOVING_AVG: int = 10  # moving average window_size (originally set to 4)

# variables for Butterworth filter
BUTTERWORTH_ORDER: int = 4  # Order of the Butterworth filter
BUTTERWORTH_CUTOFF: float = 2.0  # Cutoff frequency for the Butterworth filter
FS: int = 200  # Sampling frequency (Hz)

# variables for Derivative
FACTOR: float = 5.0   # Adjusted factor to set jerk threshold
PERCENTILE: float = 95.0    # Adjusted percentile to set jerk threshold
JERK_THRESHOLD: float = 1.0253383436586553e-08 #4.64e-07  # Threshold for significant jerk

# variables for ROI_SD method
# values can be changed  to increase/ decrease sensitivity
# WINDOW_SIZE: increase to detect over longer intervals
WINDOW_SIZE: int = 2000 # each cell is 5ms, 10000 cells represent 2secs, 2500 cells are 0.5secs. longer events 8000
STEP_SIZE: int = int(WINDOW_SIZE / 4) # 2000 cells are 400ms (0.4secs), 833 cells are 166.6ms (0.166secs). longer events 2000
#THRESHOLD: float = 0.0 # default value for SD threshold 1.5 (1.5e-08)

YMAX: float = 6e-08  # limit for vlines
YMIN: float = -6e-08  # limits for vlines