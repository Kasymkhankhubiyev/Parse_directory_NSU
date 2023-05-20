import pandas as pd
import numpy as np


MIN = 'min'
MAX = 'max'
MEAN = 'mean'
MEDIAN = 'median'


# надо передавать функцию
def _calc_IQR(data: pd.Series) -> float:
    """
    
    """
    q75, q25 = np.percentile(data, [75 ,25])
    iqr = q75 - q25

    return iqr

def _replace_series(data: pd.Series, method: str, critical_value: float) -> pd.Series:
    """
    
    """
    targets = data.values

    idx = int(np.floor(len(targets) / 2))

    median = np.sort(targets)[idx]

    if method == MIN:
        filtered = targets[np.where(targets > median + critical_value)]
        if len(filtered) == 0:
            return data
        replace_value = np.min(filtered)
    elif method == MAX:
        filtered = targets[np.where(targets > median + critical_value)]
        if len(filtered) == 0:
            return data
        replace_value = np.max(filtered)
    elif method == MEAN:
        filtered = targets[np.where(targets > median + critical_value)]
        if len(filtered) == 0:
            return data
        replace_value = np.sum(filtered) / len(filtered)
    elif method == MEDIAN:
        filtered = targets[np.where(targets > median + critical_value)]
        if len(filtered) == 0:
            return data
        replace_value = filtered[int(np.floor(len(filtered) / 2))]

    if type(targets[0]) in [int, np.int32, np.int64]:
        replace_value = int(replace_value)
    
    return pd.Series(np.where(targets > median + critical_value, replace_value, targets))
    

def replace_dropouts(data: pd.DataFrame, method=MIN, critical_distance=None) -> pd.DataFrame:
    new_data = data.copy()
    for feature in new_data.columns[:-1]:
        if (new_data[feature].dtype != 'object'):
            if critical_distance is None:
                critical_distance = _calc_IQR(new_data[feature])
            new_data[feature] = _replace_series(data=new_data[feature], method=method, critical_value=critical_distance)

    return new_data

            


            