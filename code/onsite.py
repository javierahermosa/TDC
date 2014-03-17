# TERALYTICS ONSITE DATA CHALLENGE - JAVIERA GUEDES - MARCH 2014

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as dt
import pickle

from plots import *
from tools_onsite import *

set_font()
img_dir = "../static/img/"

mallG = pickle.load(open("../data/globus_data.p", "rb"))
mallS = pickle.load(open("../data/sihlcity_data.p", "rb"))

# convert to dataframe
maG = pd.DataFrame(mallG)
maS = pd.DataFrame(mallS)

mG, mS = setup_data([maG,maS])

#plot_hour_distrib(mG, mS)
#plot_events_vs_time(mG, mS, key='time_start')

# lunch people
lunchG_a = mG[mG['time_start']>dt.time(11,50,00)]
lunchG = lunchG_a[lunchG_a['time_start']<dt.time(14,00,00)]

lunchS_a = mS[mS['time_start']>dt.time(11,50,00)]
lunchS = lunchS_a[lunchS_a['time_start']<dt.time(14,00,00)]

lunchG_ids = set(lunchG['uid'].values)
lunchS_ids = set(lunchS['uid'].values)

# percentage of people that go to the mall at lunchtime
totalG_ids = set(mG['uid'].values)
totalS_ids = set(mS['uid'].values)

# print "percentage lunch G: %s" % 100.*len(lunchG_ids)/len(totalG_ids) 
# print "percentage lunch S: %s" % 100.*len(lunchS_ids)/len(totalS_ids) 
#plot_events_vs_time(lunchG, lunchS, key='time_start')
    
def naive_durations(df, ids):
    ud = {}
    durations = []
    for i in ids:
        aa = df[df['uid']== i].groupby(['date']).agg({"duration": lambda x: x.sum()})
        for v in aa.values:
            durations.append(v[0])
    return durations

durationsG = naive_durations(lunchG, lunchG_ids)
durationsS = naive_durations(lunchS, lunchS_ids)
dG = [d for d in durationsG if d>0]
dS = [d for d in durationsS if d>0]

allG_durations = naive_durations(mG, totalG_ids)
allS_durations = naive_durations(mS, totalS_ids)
aG = [d for d in allG_durations if d>0]
aS = [d for d in allS_durations if d>0]

def plot_lunch_durations(dG, dS, gbins=200, sbins=330, label='lunch'):
    plt.hist(dG, bins=gbins, normed=True, alpha=1, color='#FF7878')
    plt.hist(dS, bins=sbins, normed=True, alpha=0.5, color= '#2396D4')
    
    plt.xlim(0,10)
    plt.xlabel('Visit Durations [hrs]')
    plt.ylabel('Normalized Counts')
    plt.title(label+' visitors')
    plt.legend( ('Mall G', 'Mall S'), loc=1)
    plt.savefig(img_dir+'naive_durations_'+label+'_onsite.png', format="png", dpi=500)
    #plt.show()
    
#plot_lunch_durations(dG, dS)
plot_lunch_durations(aG, aS, gbins=300, sbins=300, label='total')
 
# what about people that go to the cinema? How long do they stay at the mall?
cineG_a = mG[mG['time_start']>dt.time(19,50,00)]
cineG = cineG_a[cineG_a['time_start']<dt.time(20,30,00)]

cineS_a = mS[mS['time_start']>dt.time(19,50,00)]
cineS = cineS_a[cineS_a['time_start']<dt.time(20,30,00)]

cineG_ids = set(cineG['uid'].values)
cineS_ids = set(cineS['uid'].values)

# percentage of people that go to the mall at 8pm (late movietime)
totalG_ids = set(mG['uid'].values)
totalS_ids = set(mS['uid'].values)

print 100.*len(cineG_ids)/len(totalG_ids)
print 100.*len(cineS_ids)/len(totalG_ids)

dinnerG_a = mG[mG['time_start']>dt.time(17,50,00)]
dinnerG = dinnerG_a[dinnerG_a['time_start']<dt.time(19,50,00)]

dinnerS_a = mS[mS['time_start']>dt.time(17,50,00)]
dinnerS = dinnerS_a[dinnerS_a['time_start']<dt.time(19,50,00)]

dinnerG_ids = set(dinnerG['uid'].values)
dinnerS_ids = set(dinnerS['uid'].values)

print 100.*len(dinnerG_ids)/len(totalG_ids)
print 100.*len(dinnerS_ids)/len(totalG_ids)

dinner_cineG = [c for c in cineG_ids if c in dinnerG_ids]
dinner_cineS = [c for c in cineS_ids if c in dinnerS_ids]

print 100.* len(dinner_cineG)/len(cineG_ids)
print 100.* len(dinner_cineS)/len(cineS_ids)
