# TERALYTICS ONSITE DATA CHALLENGE - JAVIERA GUEDES - MARCH 2014

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime as dt
import collections
from scipy import stats

def timestamp_to_df(timestamps):
    return [dt.datetime.fromtimestamp(el) for el in timestamps]

def get_time(timestamps):
    return [el.time() for el in timestamps]

def get_date(timestamps):
    return [el.date() for el in timestamps]

def get_hour(dates):
    return [d.hour for d in dates]
            
def setup_data(df_list):
    for df in df_list:
        df['start'] = timestamp_to_df(df['start'])
        df['end'] = timestamp_to_df(df['end'])
        df['duration'] = (df['end']-df['start'])/np.timedelta64(1, 'h')
        df['time_start'] = get_time(df['start'])
        df['time_end'] = get_time(df['end'])
        df['date'] = get_date(df['start'])
        df['hour'] = get_hour(df['start'].tolist())
        
    return df_list[0], df_list[1]

def normalize_counts(df_days):
    a = df_days.value_counts()
    b = a.sort_index()
    return b.index, 1.*b.values/len(df_days)