# TERALYTICS DATA CHALLENGE - JAVIERA GUEDES - MARCH 2014

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as dt

from plots import *
from tools import *

mallG = pd.read_csv("../data/mallG.csv")
mallS = pd.read_csv("../data/mallS.csv")

mG, mS = setup_data([mallG, mallS])

############## BASICS ################

# 1. Size of the dataset
print "size Mall G dataset: %s" % len(mG)
print "size Mall G dataset: %s" % len(mS)

# 2. Unique users over the two-week period
unique_users_G = len(set(mallG['uid']))
unique_users_S = len(set(mallS['uid']))

# 3. Percentage of unique users over the two-week period 
fraction_unique_G = fraction_unique(mG, unique_users_G)
fraction_unique_S = fraction_unique(mS, unique_users_S)

plot_pie([fraction_unique_G, 1-fraction_unique_G], title="Mall G")
plot_pie([fraction_unique_S, 1-fraction_unique_S], title="Mall S")

# 4. Visit durations
print "Median and mean visit durations Mall G: %s, %s" % \
        (np.median(mG['duration']), np.mean(mG['duration']))
print "Median and mean visit durations Mall S: %s, %s" % \
        (np.median(mS['duration']), np.mean(mS['duration']))

# 5. Typical number of events
evG=mallG['events'].value_counts()
evS=mallG['events'].value_counts()
print "Typical Number of Events Mall G, Mall S: %s, %s" % \
        (len(evG), len(evS))

# lots of events 
a=mallG['events'].value_counts().index
b=mallS['events'].value_counts().index
print "Frequency of > 100 events Mall G and Malls S:  %s, %s" % \
            (len(a[a>100]), len(b[b>100]))

# 6. Common users?
mG_ids = mG['uid'].values.tolist()
mS_ids = mS['uid'].values.tolist()

ids_GS = intersect(mG_ids, mS_ids)

############## CHALLENGE ################

# 1. Visit Durations
plot_visit_durations(mG, mS)
boxplots(mG, mS, key='duration')

#2. Number of Events
plot_events(mG, mS)
boxplots(mG, mS, key="events")

# Visit Duration v.s. Number of Events
plot_events_vs_duration(mG, mS)
plot_events_vs_time(mG, mS)

#3. Unique and Frequent Visitors per day / per week

# Calculate the average number of unique visitors per day excluding sundays
u_workday = mG[mG['weekday'] != 7].groupby(['date']).agg({"uid": pd.Series.nunique})
avg = np.mean(u_workday)

# 3a. Calculate the total number of visits per day 
pu_dayG, cG = unique_visitors(mG, key='date')
pu_dayS, cS = unique_visitors(mS, key='date')

plot_unique_visitors_day(mG, mS)

# mean percentage of unique visitors per day
mu_day_G = np.mean([v for (k,v) in pu_dayG.items()])/100.
mu_day_S = np.mean([v for (k,v) in pu_dayS.items()])/100.
   
plot_pie([mu_day_G, 1-mu_day_G], title="Mall G", file='_per_day')
plot_pie([mu_day_S, 1-mu_day_S], title="Mall S", file='_per_day')

# 3b. Calculate the total number of visits per week
pu_weekG, cG = unique_visitors(mG, key='week')
pu_weekS, cS = unique_visitors(mS, key='week')

# mean percentage of unique visitors per week
mu_week_G = np.mean([v for (k,v) in pu_weekG.items()])/100.
mu_week_S = np.mean([v for (k,v) in pu_weekS.items()])/100.
   
plot_pie([mu_week_G, 1-mu_week_G], title="Mall G", file='_per_week')
plot_pie([mu_week_S, 1-mu_week_S], title="Mall S", file='_per_week')

# 3c. Frequent visitors per day
fvG_day = mG.groupby(['date'])['uid'].apply(count_frequent)
fvS_day = mS.groupby(['date'])['uid'].apply(count_frequent)
plot_frequent_visitors(fvG_day, fvS_day, label='day')

# 3d. Frequent visitors per week
fvG_week = mG.groupby(['week'])['uid'].apply(count_frequent)
fvS_week = mS.groupby(['week'])['uid'].apply(count_frequent)
plot_frequent_visitors(fvG_week, fvS_week, label='week')

# ids of the frequent visitors
fvG_ids = set([f[1] for f in fvG_day.index])
fvS_ids = set([f[1] for f in fvS_day.index])

# 4. Find employees
fvG, seG = find_employees(mG,fvG_ids)
plot_employees(fvG,seG, 'Mall G')

fvS, seS = find_employees(mS,fvS_ids)
plot_employees(fvS,seS, 'Mall S')
    
plot_daily_schedule(mG, seG, 'Mall G')
plot_daily_schedule(mS, seS, 'Mall S')

############## BEYOND ################

#1, 2. Residence Graphs    
nodeG, linkG = residency_tree(mG, 2)
nodeS, linkS = residency_tree(mS, 20)

# 3. where do employees live?
emG_zips = zip_employees(mG, seG)
emS_zips = zip_employees(mS, seS)

# 4a. What's the distribution of times at which people go to the mall?
plot_hour_distrib(mG, mS, time='start')

# 4b. What days of the week do people go to the mall most?
plot_day_distrib(mG, mS)

# 5. night visitors
nvG = set(mG[mG['time_end']>dt.datetime(1900,1,1,23,0,0).time()]['uid'])
nvS = set(mS[mS['time_end']>dt.datetime(1900,1,1,23,0,0).time()]['uid'])
e_nvG = [e for e in seG.keys() if e in nvG]
e_nvS = [e for e in seS.keys() if e in nvS]

# percent of employees who are "night visitors"
pe_nvG = 100.*len(e_nvG)/len(seG)
pe_nvS = 100.*len(e_nvS)/len(seS)
print pe_nvG, pe_nvS



