#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:43:08 2020

@authors: Joseph Martin, University of Victoria
Kelsey Shaw, University of Victoria
Andrew Freiburger, University of Victoria
"""
import pandas as pd
import KWE as KWE
import ADRE as ADRE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import calendar


date_range=[pd.Timestamp('2010-01-01'), pd.Timestamp('2010-04-01')]
data=pd.read_csv("Data/Lake_Cowichan_Historical_Daily.csv") #daily historical data
del data["PARAM"], data["SYM"], data[" ID"]
data["Date"]=pd.to_datetime(data["Date"])
data=data.where((data["Date"]>=date_range[0]) & (data["Date"] <= date_range[1])).dropna(axis=0)

data_down=pd.read_csv("Data/Duncan_Historical_Daily.csv") #daily historical data
del data_down["PARAM"], data_down["SYM"], data_down[" ID"]
data_down["Date"]=pd.to_datetime(data_down["Date"])
data_down=data_down.where((data_down["Date"]>=date_range[0]) & (data_down["Date"] <= date_range[1])).dropna(axis=0)

C_month=pd.read_csv("Data/Monthly_Nitrogen_Loading.csv")
time_min=0.5 #delta t
dist_step=3800 #delta x
length=38000+dist_step #River Length
width=25 #River Width
slope=0.005
roughness=0.035 #Manning’s roughness constant (this is Lehigh River value)'
decay_coeff=0.015 
disp_coeff=7.5

"Expand and interpolate downstream observations this is done inside the KWE function for upstream observations"
start=data_down.iloc[0,0]
end=data_down.iloc[(len(data_down)-1),0]     
x=data_down.set_index(pd.to_datetime(data_down["Date"]))
del x["Date"]
# del x[u'Parameter ']
new_index = pd.date_range(start, end, freq=('%smin' % time_min))   
dd=x.reindex(new_index).interpolate()

print(data)
#%%
lat_flows=pd.DataFrame([[8000,pd.Timestamp('2020-03-17T07'),0],[25000,pd.Timestamp('2020-03-20T06'),0],[32000,pd.Timestamp('2020-03-18T09'),0]])
"""Inflows and outflows for point sources can be put into the DataFrame in the format [distance along river, time 
(type Timestamp), Q_cfs]. Any number can be put in.  Currently this is not in use, but could be used for the
Crofton pulp mill."""

#test=KWE.route(time_min, dist_step, length, width, slope, roughness, data, lat_flows) #returns the q route matrix

"""This block is temporary until proper velocities are calculated."""
diststep=[] 
k=0
while dist_step*k<=length: #This would be done inside the KWE function normally.
	diststep.append(dist_step*k)
	k+=1
v_matrix=pd.DataFrame(0.003, index=dd.index, columns=diststep) #"Model-friendly" velocity

print(v_matrix)

flow_depth=0.09 #A rough average based on KWE calculations, ideally this would be returned from KWE 

C=ADRE.route(time_min, dist_step, width, flow_depth, v_matrix, disp_coeff, decay_coeff)

"""Plot the hydrographs of various distance steps on the same plot -
19000 and 26600 have means printed vice plotting in order to maintain scale."""

x=C.index
fig, ax = plt.subplots()
for d in diststep:
    if d==length:
        break
    elif d==22800:
        ax.plot(C.index, C[d], label="ALR2")
    elif d==30400:
        ax.plot(C.index, C[d], label="ALR3")
    elif d==0:
        ax.plot(C.index, C[d], label="Upstream")
    elif d==26600:
        print C[d].mean()
    elif d==19000:
        print C[d].mean()
    elif d==(length-dist_step):
        ax.plot(C.index, C[d], label="Downstream")
    else:
        ax.plot(C.index, C[d], label=("%i" % d))
plt.xlabel("Time (Day and Hour) - timestep = %.2f min" % time_min)	
fig.autofmt_xdate(bottom=None, rotation=30)
plt.ylabel("Concentration (mg/L)")
plt.title("Nitrate Concentrations at Lake Cowichan and Duncan from %s %s to %s %s" % ((calendar.month_name[start.month]), start.year ,(calendar.month_name[end.month]), end.year))
plt.legend()
plt.show()


                    

