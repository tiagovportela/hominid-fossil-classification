import pandas as pd
import numpy as np
import math

from statistics import mode

def read_csv_file(file_name):
    return pd.read_csv(file_name)

# functyion that aggragate by input column and use the function to aggregate
def aggregate_data(data, column_name, func = 0):
    data_frame = data.copy()
    grouped = data_frame.groupby(column_name)
    agg_dict = {}
    for col in data_frame.columns:
        if data_frame[col].dtype == 'float64':
            agg_dict[col] = "mean"
        elif func != 0:
            agg_dict[col] = lambda x: func(x)
    result = grouped.agg(agg_dict)#.reset_index(drop=True)
    return result.copy()


        

