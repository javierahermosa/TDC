# TERALYTICS DATA CHALLENGE - JAVIERA GUEDES - MARCH 2014

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime as dt
import collections
from scipy import stats

def set_font():
    matplotlib.rcParams.update({'font.size': 17, 
    'font.family': 'serif', 'sans-serif':['Helvetica']})

def intersect(a, b):
    return list(set(a) & set(b))
        
def get_hour(dates):
    return [d.hour for d in dates]

def get_time(timestamps):
    return [el.time() for el in timestamps]

def get_week(dates):
    week = []
    for d in dates:
        if d < dt.datetime(2014,1,20).date():
            week.append(1)
        else:
            week.append(2)    
    return week
    
def get_weekday(dates):
    return [d.isoweekday() for d in dates]

def get_date(timestamps):
    return [el.date() for el in timestamps]

def quantile(data, q):
    N, bins = np.histogram(data, bins=np.sqrt(len(data)))
    norm_cumul = 1.0 * N.cumsum() / len(data)
    return bins[norm_cumul > q][0]
    
def normalize_counts(df_days):
    a = df_days.value_counts()
    b = a.sort_index()
    return b.index, 1.*b.values/len(df_days)
    
# Calculates the basic statistics of a distribution        
def basic_stats(df, key):
    mu = np.mean(df[key])
    median = np.median(df[key])
    sigma = np.std(df[key])
    iqr = quantile(df[key],0.75) - quantile(df[key],0.25)
    mode = stats.mode(df[key].values)
    return mu, median, sigma, iqr, mode
   
# Add features to the dataframes to facilitate de analysis    
def setup_data(df_list):
    for df in df_list:
        df['start'] = pd.to_datetime(df['start'])
        df['end'] = pd.to_datetime(df['end'])
        df['duration'] = (df['end']-df['start'])/np.timedelta64(1, 'h')
        
        start_list = df['start'].tolist()
        df['weekday'] = get_weekday(df['start'].tolist())
        
        df['date'] = get_date(df['start'])
        df['time'] = get_time(df['start'])
        df['time_end'] = get_time(df['end'])
        df['hour'] = get_hour(df['start'].tolist())
        df['week'] = get_week(df['date'].values.tolist()) 
    return df_list[0], df_list[1]
        
def count_unique(x):
    c = x.value_counts()
    return c[c== 1]
    
def count_frequent(x):
    c = x.value_counts()
    return c[c> 1]

# Calculate the fraction of unique users
def fraction_unique(df, unique_users):
    nvisits = df['uid'].value_counts().values
    unique_visits = len(nvisits[nvisits==1])
    fraction_unique = 1.* unique_visits / unique_users
    return fraction_unique

# Unique user IDs per day (key='date') or per week (key='week')        
def unique_visitors(df, key='date'):

    u_day=df.groupby([key]).agg({"uid": pd.Series.nunique})
    dates = u_day.index
    u_values = [u[0] for u in u_day.values]
    u_day_dict = dict(zip(dates,u_values))
    
    # unique visitors    
    uv = df.groupby([key])['uid'].apply(count_unique)
    idx = uv.index

    # make a dictionary that contains the date as key and 
    # the number of unique visitor as value
    dates = set(df[key].values)
    # number of users that visit the mall once per day
    uv_counts = {}
    uv_ids = {}
    uv_percent = {}
    for d in dates:
        uv_counts[d] = len([u[1] for u in idx if u[0]==d])
        uv_ids[d] = [u[1] for u in idx if u[0]==d] 
        uv_percent[d] = 100.* uv_counts[d]/u_day_dict[d]
    
    # percentage of unique visitors sorted by date
    up = collections.OrderedDict(sorted(uv_percent.items()))
    uc = collections.OrderedDict(sorted(uv_counts.items()))
    return up, uc 


# model for finding employees:
# They are "frequent users" that appear at the mall 
# Over 4 days a week in average
# Over 20 hours a week in average
# Stay for over 4 hours at the mall each day         
def find_employees(df, ids):
    fv = {}
    se = {}
    for fid in ids:
         aa = df[df['uid']== fid].groupby(['date']).agg({"duration": lambda x: x.sum()})
         v_date = aa.index
         ndays = len(v_date)/2.
         v_duration = sum([d[0] for d in aa.values])/2.
         avg_duration = np.mean([d[0] for d in aa.values])
         fv[fid] = (ndays, v_duration, avg_duration)
         
         if ndays > 3.75 and v_duration > 20 and avg_duration > 4: 
            start = []
            end = []
            bb =  df[df['uid']==fid][['time','time_end', 'date']]
            for date in v_date:
                start.append(min(bb[bb['date']==date]['time']))
                end.append(max(bb[bb['date']==date]['time_end']))
                 
            se[fid] = (v_date, start, end)
    return fv, se

# Calculates the average of datetime objects 
def avg_time(times):
    avg, std2 = 0, 0 
    avg = np.int(np.mean([t.second + 60*t.minute + 3600*t.hour for t in times]))
    std = np.int(np.std([t.second + 60*t.minute + 3600*t.hour for t in times]))
    rez = str(avg/3600) + ' ' + str((avg%3600)/60) + ' ' + str(avg%60)
    return dt.datetime.strptime(rez, "%H %M %S"), dt.timedelta(seconds=std)

# Get the zipcodes of the employees
def zip_employees(df, se):
    em_zip = []
    em_ids = se.keys()
    for em in em_ids:
        em_zip.append(df[df['uid']==em]['residence'].values[0])
    return em_zip

# D3 residence graph uses nodes and links
# nodes will be grouped by zipcode. For example zipcodes 
# between 1000 and 1099 belong to group 10
def residency_tree(df, min):

    res = df['residence'].value_counts()
    r2 = res[res>min]
    n_nodes = len(r2)
    
    zips = r2.index.tolist()
    counts = r2.values.tolist()
    
    nodes = []
    groups = []
    for z,v in zip(zips,counts):
        nodes.append({"name":str(z), "group":z/100, "size":str(v)})
        groups.append(z/100)
    
    # the most frequent zipcode (fz) in each group is connected to the root
    # first, get the most common zipcode in each group
    fz = {}
    dic =  dict(zip(zips, counts))
    
    for k,v in dic.items():
        g = k/100
        if g in fz.keys():
            if  fz[g][1] < v:
                fz[g] = (k,v)
        else:
            fz[g] = (k,v)
    
    links = []
    for z,v in fz.items():
        links.append({"source":zips.index(v[0]), "target":0, "value":5})
    
    # every minor zipcode in each group is connected to fz    
    for z in zips:
        g = z/100
        if z not in fz.keys():
            links.append({"source":zips.index(z), "target":zips.index(fz[g][0]), "value":10})   
            
    # Consecutive zipcodes are connected 
    for g,v in fz.items():
        if g+1 in fz.keys():
            links.append({"source":zips.index(v[0]), "target":zips.index(fz[g+1][0]), "value":1}) 
    
    
    return nodes, links