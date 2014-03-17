# TERALYTICS DATA CHALLENGE - JAVIERA GUEDES - MARCH 2014

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import numpy as np
import datetime as dt
from tools import *

set_font()
img_dir = "../static/img/"
    
# Challenge Figure 1
def plot_visit_durations(mG, mS):  
    
    muG, medianG, stdG, iqrG, modeG = basic_stats(mG, 'duration')
    muS, medianS, stdS, iqrS, modeS = basic_stats(mS, 'duration')
     
    fig, ax = plt.subplots()
    
    mG['duration'].hist(bins=50, normed=True, alpha=1, color='#FF7878', grid=False)
    mS['duration'].hist(bins=50, normed=True, alpha=0.7, color= '#2396D4', grid=False)
    
    textG = 'Mall G\n\n$\mu=%.2f$\n$\sigma=%.2f$\n$\mathrm{mode}=%.2f$\n$\mathrm{median}=%.2f$\n$\mathrm{IQR}=%.2f$'%(muG, stdG, modeG[0], medianG, iqrG)
    textS = 'Mall S\n\n$\mu=%.2f$\n$\sigma=%.2f$\n$\mathrm{mode}=%.2f$\n$\mathrm{median}=%.2f$\n$\mathrm{IQR}=%.2f$'%(muS, stdS, modeS[0], medianS, iqrS)
    propsG = dict(boxstyle='round', fc = "w", ec='#FF7878', alpha=1)
    propsS = dict(boxstyle='round', fc = "w", ec='#2396D4', alpha=1)
    ax.text(0.45, 0.95, textG, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', ha='left', bbox=propsG)
    ax.text(0.7, 0.95, textS, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', ha='left', bbox=propsS)
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    ax.set_axisbelow(True)
    plt.ylabel('Probability Density')
    plt.xlabel('Duration of the Visits [hrs]')
    plt.savefig(img_dir+'duration_distrib.png', format="png", dpi=500 )

# Challenge Figure 2, 4
def boxplots(mG, mS, key = 'duration', labels = ['Mall G', 'Mall S'] ):
    
    data_A = mG[key].values.tolist()
    data_B = mS[key].values.tolist()
    min_AB = min(min(data_A), min(data_B))
    max_AB = max(max(data_A), max(data_B))
    data = [data_A, data_B]
    
    fig, ax = plt.subplots()
    
    bp = plt.boxplot(data, positions=[1,2], widths = 0.5)
    
    plt.setp(bp['medians'][0], color='#FF7878', linewidth=1.5)
    plt.setp(bp['medians'][1], color='#2396D4', linewidth=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'][0], color='#FF7878', marker='o')
    plt.setp(bp['fliers'][2], color='#2396D4', marker='o')
    ax.set_xticklabels(labels)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    if key == 'duration':
        plt.ylabel('Duration of the Visits [hrs]')
        ax.set_ylim(-0.5, 1.1 * max_AB)
    elif key == 'events':
        plt.ylabel('Number of Events')
        ax.set_ylim(-10, 1.1 * max_AB)
    plt.savefig(img_dir+key+'_boxplots.png', format="png", dpi=500)
    
# Challenge Figure 3
def plot_events(mG, mS):
    
    muG, medianG, stdG, iqrG, modeG = basic_stats(mG, 'events')
    muS, medianS, stdS, iqrS, modeS = basic_stats(mS, 'events')
    
    fig, ax = plt.subplots()
    
    mG['events'].hist(bins=95, normed=True, alpha=1, color='#FF7878', grid=False)
    mS['events'].hist(bins=270, normed=True, alpha=0.7, color= '#2396D4', grid=False)
    mG['events'].plot(kind='kde', xlim=(0,120),color='#FF7878', linewidth=2)
    mS['events'].plot(kind='kde', xlim=(0,120),color= '#2396D4', linewidth=2)

    textG = 'Mall G\n\n$\mu=%.2f$\n$\sigma=%.2f$\n$\mathrm{mode}=%.2f$\n$\mathrm{median}=%.2f$\n$\mathrm{IQR}=%.2f$'%(muG, stdG, modeG[0], medianG, iqrG)
    textS = 'Mall S\n\n$\mu=%.2f$\n$\sigma=%.2f$\n$\mathrm{mode}=%.2f$\n$\mathrm{median}=%.2f$\n$\mathrm{IQR}=%.2f$'%(muS, stdS, modeS[0], medianS, iqrS)
    propsG = dict(boxstyle='round', fc = "w", ec='#FF7878', alpha=1)
    propsS = dict(boxstyle='round', fc = "w", ec='#2396D4', alpha=1)
    ax.text(0.45, 0.95, textG, transform=ax.transAxes, fontsize=14,
            va='top', ha='left', bbox=propsG)
    ax.text(0.7, 0.95, textS, transform=ax.transAxes, fontsize=14,
            va='top', ha='left', bbox=propsS)
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    ax.set_axisbelow(True)
    plt.ylabel('Probability Density')
    plt.xlabel('Number of Events')
    plt.savefig(img_dir+'event_distrib.png', format="png", dpi=500 )
    
# Challenge Figure 5
def plot_events_vs_duration(mG, mS):
     fig, (ax1, ax2) = plt.subplots(1,2, sharey=True, sharex=True)
     xG = mG['duration'].values
     yG = mG['events'].values
     xS = mS['duration'].values
     yS = mS['events'].values

     ax1.plot(xG,yG, 'ro', alpha=0.3)
     ax2.plot(xS,yS, 'o', color= '#2396D4', alpha=0.3)
     
     ax1.text(0.15, 0.95, 'Mall G', transform=ax1.transAxes, fontsize=14,
             verticalalignment='top', ha='left', color= '#FF7878')
     ax2.text(0.15, 0.95, 'Mall S', transform=ax2.transAxes, fontsize=14,
            verticalalignment='top', ha='left', color='#2396D4')
     ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
     ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
     ax1.set_axisbelow(True)
     ax2.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
     ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
     ax1.set_xlabel('Visit Duration [hrs]')
     ax2.set_xlabel('Visit Duration [hrs]')
     ax1.set_ylabel('Number of Events')
     ax2.set_axisbelow(True)
     plt.savefig(img_dir+'event_vs_duration.png', format="png", dpi=500)
   
# Challenge Figure 6
def plot_events_vs_time(mG, mS, key='time'):

     xG = [(x.hour *3600 + x.minute*60 + x.second)/3600. for x in mG[key].values]
     yG = mG['events'].values
     xS = [(x.hour *3600 + x.minute*60 + x.second)/3600. for x in mS[key].values]
     yS = mS['events'].values
     
     fig, (ax1, ax2) = plt.subplots(1,2, sharex=True)
          
     ax1.plot(xG,yG, 'ro', alpha=0.3)
     ax2.plot(xS,yS, 'o', color= '#2396D4', alpha=0.3)
     ax1.text(0.15, 0.95, 'Mall G', transform=ax1.transAxes, fontsize=14,
             verticalalignment='top', ha='left', color= '#FF7878')
     ax2.text(0.15, 0.95, 'Mall S', transform=ax2.transAxes, fontsize=14,
            verticalalignment='top', ha='left', color='#2396D4')
     ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
     ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
     ax1.set_axisbelow(True)
     ax2.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
     ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
     ax2.set_axisbelow(True)

     ax2.set_xlim([0,24])
     ax1.set_xlabel('Time of the Day')
     ax2.set_xlabel('Time of the Day')
     ax1.set_ylabel('Number of Events')
     plt.savefig(img_dir+'event_vs_time_onsite.png', format="png", dpi=500)

# Challenge Figure 6 (alternative)     
def plot_events_vs_time2(mG, mS):

     aG = mG.groupby(['hour']).agg({"events": lambda x: x.count()})
     aS = mS.groupby(['hour']).agg({"events": lambda x: x.count()})
     
     fig, ax = plt.subplots()
     plt.plot(aG.index, aG.values, 'o-', color ='#FF7878')
     plt.plot(aS.index, aS.values, 'o-', color = '#2396D4')
     ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                       alpha=0.5)
     ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                       alpha=0.5)
     ax.legend( ('Mall G', 'Mall S'), loc=2)
     plt.ylabel('Number of Events per Hour')
     plt.xlim([0,24])
     plt.ylim([0,6000])
     plt.xlabel('Time of the Day [hr]')
     plt.savefig(img_dir+'event_vs_time_bins.png', format="png", dpi=500)

# Basics Figure 1, Challenge Figures 7, 9
def plot_pie(sizes, title="Mall", file=''):
    fig, ax = plt.subplots()
    labels = 'One Visit', 'Frequent Visits'
    colors = ['#2396D4', '#FF7878']
    explode = (0, 0.1) 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=90)
    plt.axis('equal')
    left, width = .01, .5
    bottom, height = .1, .85
    right = left + width
    top = bottom + height
    ax.text(left, top, title,
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax.transAxes,
        fontsize=32)
    plt.savefig(img_dir+"pie_visitors_"+title.replace(" ", "")+file+".png", 
                format="png", dpi=500 )

# Challenge Figure 8
def plot_unique_visitors_day(mG, mS):
    pu_dayG, cG = unique_visitors(mG)
    pu_dayS, cG = unique_visitors(mS)
    
    fig, ax = plt.subplots()
    
    p1=plt.plot(pu_dayG.keys(), pu_dayG.values(), 'o-', color='#FF7878')
    p2=plt.plot(pu_dayS.keys(), pu_dayS.values(), 'o-', color='#2396D4')
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)
    ax.set_xlabel('Date')
    ax.set_ylabel('Percent of Unique Visitors')
    hfmt = md.DateFormatter('%m.%d')
    ax.xaxis.set_major_formatter(hfmt)
    ax.set_ylim(70,100)
    plt.xticks(rotation=20)
    ax.legend( ('Mall G', 'Mall S'), loc=3)
    fig.tight_layout()
    plt.savefig(img_dir+'percent_unique.png', format="png", dpi=500)

# Challenge Figure 10    
def plot_frequent_visitors(fvG, fvS, label='day'):
    fig, ax = plt.subplots()
    
    nbins =  len(set(fvG.values))
    plt.hist([fvG, fvS], normed=True, bins=nbins, alpha=1, 
                color=['#FF7878','#2396D4'], linewidth=0.5, fill=True)
    
    plt.ylabel('Normalized Counts')
    plt.xlim(2,max(fvG.values))
    plt.xlabel('Frequency of Visitors')
    plt.title('Frequent visits per '+label)
    ax.legend( ('Mall G', 'Mall S'), loc=1)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)
    ax.set_axisbelow(True)
    plt.savefig(img_dir+'frequency_visits_'+label+'.png', format="png", dpi=500)

# Challenge Figure 11
def plot_employees(fv, se, label):
    
    # frequent users
    freq=map(list, zip(*fv.values()))
    
    # employees
    e = [v for k, v in fv.items() if k in se.keys()]
    empl = map(list, zip(*e))
    fig, ax = plt.subplots()
    
    plt.plot(freq[0],freq[1],'o', color='gray', alpha=0.7)
    if label == 'Mall G': col='#FF7878' 
    else: col= '#2396D4'
    plt.plot(empl[0], empl[1], 'o', color=col)
    
    ax.text(0.67, 0.9, 'Employees', transform=ax.transAxes, fontsize=16,
            va='top', ha='left', color= col)
    ax.text(0.1, 0.9, label, transform=ax.transAxes, fontsize=24,
            va='top', ha='left', color='gray')
    plt.vlines(3.75, 20, 42, color=col, linewidth=3)
    plt.hlines(20, 3.75, 7, color=col, linewidth=3)
    plt.xlim(0,7)
    plt.ylim(0,42)
    plt.title('Behavior of Frequent Visitors')
    plt.ylabel('Average number of hours per week')
    plt.xlabel('Average number of days per week')
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)
    ax.set_axisbelow(True)
    plt.savefig(img_dir+'employees_'+label.replace(" ",'')+'.png', format="png", dpi=500)
    
# Challenge Figure 12      
def plot_daily_schedule(df, se, label):
    
    n = se.values()
               
    fig, ax = plt.subplots()

    av_start = []
    av_end = []
    for i in range(len(se)):
        dates = n[i][0]
        t_start = n[i][1]
        t_end = n[i][2]
        # plot date vs. start time
        plt.plot(dates, t_start , 'o', color='#2396D4', alpha=0.5)
        # plot date vs. end time
        plt.plot(dates, t_end, 'o', color='#FF7878', alpha=0.5)
        
        avg_start, std_start = avg_time(t_start)
        avg_end, std_end = avg_time(t_end)
        
        av_start.append(avg_start)
        av_end.append(avg_end)

    total_avg_start, total_std_start = avg_time(av_start)
    total_avg_end, total_std_end = avg_time(av_end)
        
    tmin_start = (total_avg_start - total_std_start).time()   
    tmax_start = (total_avg_start + total_std_start).time() 
    tmin_end = (total_avg_end - total_std_end).time()   
    tmax_end = (total_avg_end + total_std_end).time() 
   
    p = plt.axhspan(tmin_start, tmax_start, fc='#2396D4', ec='#2396D4' , alpha=0.3)
    p = plt.axhspan(tmin_end, tmax_end, fc= '#FF7878', ec='#FF7878', alpha=0.3)
    
    a0 = dt.datetime(1900,1,1,1,0,0)
    dr = [a0 + dt.timedelta(hours=a) for a in range(24) if a%3==0]   
    dr2 = [t.time() for t in dr] 
    
    plt.ylim(dt.datetime(1900,1,1,0,0,0).time(),dt.datetime(1900,1,1,23,59,59).time())
    plt.xticks(rotation=20)
    ax.set_yticks(dr2)
    hfmt = md.DateFormatter('%m.%d')
    ax.xaxis.set_major_formatter(hfmt)
    plt.ylabel('Time of day [hr]')
    plt.title('Daily Work Schedule')
    ax.text(0.02, 0.9, label, transform=ax.transAxes, fontsize=24,
            va='top', ha='left', color='gray')
    plt.xlim(min(df.date)- dt.timedelta(days=4), max(df.date) + dt.timedelta(days=1))
    plt.xlabel('Date')
    plt.text(0.03,0.365, "start work", ha='left', transform=ax.transAxes, 
            color='#1F1AB2', fontsize=12)
    plt.text(0.03,0.675, "leave work", ha='left', transform=ax.transAxes, 
            color='#AB2B52', fontsize=12)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    plt.savefig(img_dir+'schedule_'+label.replace(" ",'')+'.png', format="png", dpi=500)

# Beyond Figure 3 (left)
def plot_day_distrib(mG, mS):
    
    xG,yG = normalize_counts(mG['weekday'])
    xS,yS = normalize_counts(mS['weekday'])
    
    fig, ax = plt.subplots()

    plt.plot(xG,yG,'o-', color='#FF7878', linewidth=2, markersize=10)
    plt.plot(xS,yS, 'o-', color='#2396D4', linewidth=2, markersize=10)
    ax.set_ylim(0, 0.3)
    ax.set_xticklabels(['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
    plt.ylabel('Normalized Counts')
    plt.xlabel('Day of the Week')
    ax.legend( ('Mall G', 'Mall S'), loc=2)
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    ax.set_axisbelow(True)
    plt.savefig(img_dir+'plot_day_distrib.png', format="png", dpi=500 )

# Beyond Figure 3 (right)
def plot_hour_distrib(mG, mS, time='start'):
    
    hourG = get_hour(mG[time].tolist())
    hourS = get_hour(mS[time].tolist())
    
    fig, ax = plt.subplots()
    
    plt.hist([hourG, hourS], bins=24, normed=True, alpha=1, 
                color=['#FF7878','#2396D4'], linewidth=0.5, fill=True)
    
    ax.set_xlim(0, 24)
    plt.ylabel('Normalized Counts')
    plt.xlabel('Time of day')
    ax.legend( ('Mall G', 'Mall S'), loc=2)
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    ax.set_axisbelow(True)
    plt.savefig(img_dir+'plot_hour_distrib_onsite.png', format="png", dpi=500 )


