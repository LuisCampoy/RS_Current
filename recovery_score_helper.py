# Recovery Score Calculations: recovery score calculator
# Script created 5/29/2024
# Last revision 5/23/2025

import numpy as np

def get_rs_sa(sa_2axes: float) -> float:
    '''
    Calculates the Recovery Score for SA based on sa_2axes.
    The formula is based on the long Term RS Regression. 
    This formula can be updated as needed.

    Args:
        sa_2axes (float): numerical value for the SA Recovery Score

    Returns:
        float: result of the calculation when there is only one single successful attempt
    '''

    recovery_score_sa: float = np.exp(0.080714 * sa_2axes)

    return recovery_score_sa

def get_rs_ua(sa_2axes: float, sumua: float) -> float:
    '''
    Calculates the Recovery Score for UA based on sa_2axes and sumua.

    Args:
        sa_2axes (float): numerical value for the SA Recovery Score
        sumua (float): numerical value for the UA Recovery Score

    Returns:
        float: result of the calculation when there is only one single successful attempt
    '''

    recovery_score_ua: float = 7.0312 * np.power(sumua, 0.278)

    return recovery_score_ua