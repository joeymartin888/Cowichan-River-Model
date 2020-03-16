#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:43:08 2020

@author: Joseph Martin, University of Victoria
"""
import pandas as pd
import KWE as KWE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.dates as mdates

data=pd.read_csv("River_routing_data.csv") #using the Assignment 3 Data right now...
length=52800 #River Length
width=300 #River Width
time_min=3 #delta t
dist_step=5280 #delta x
slope=0.005
roughness=0.025 #Manning’s roughness constant (this is Lehigh River value)'
k=0.2
E=0.5

lat_flows=pd.DataFrame([[8000,pd.Timestamp('2008-03-06T07'),0],[10000,pd.Timestamp('2008-03-05T06'),0],[52000,pd.Timestamp('2008-03-06T09'),0]])
"""Inflows can be put into the DataFrame in the format [distance along river, time 
(type Timestamp), Q_cfs]. Any number can be put in."""

test=KWE.route(time_min, dist_step, length, width, slope, roughness, data, lat_flows) #returns the q route matrix
v_matrix=test/90000 #Arbitrary cross section

diststep=[]
k=0
while dist_step*k<=length:
	diststep.append(dist_step*k)
	k+=1
    
C=pd.DataFrame(0, index=range(len(v_matrix)), columns=diststep)
C.iloc[5,0]=100.0
    
for j in range(len(v_matrix)-1):
        for i in range(len(diststep)-1):
            w1=(1.0/(2.0*time_min))-(v_matrix.iloc[j,i]/(2.0*dist_step))-(E/(dist_step**2.0))-(k/4.0)
            w2=(1.0/(2.0*time_min))-(v_matrix.iloc[j,i+1]/(2.0*dist_step))+(E/(2.0*(dist_step**2.0)))-(k/4.0)
            w3=(-1.0/(2.0*time_min))-(v_matrix.iloc[j+1,i]/(2.0*dist_step))-(E/(dist_step**2.0))-(k/4.0)
            w4=(-1.0/(2.0*time_min))-(v_matrix.iloc[j+1,i+1]/(2.0*dist_step))+(E/(2*(dist_step**2.0)))-(k/4.0)
            C.iloc[j+1,i+1]=(-1.0/w4)*(w1*C.iloc[j,i]+w2*C.iloc[j,i+1]+w3*C.iloc[j,i+1]+(E/(2*(dist_step**2)))*C.iloc[j,i-1]+(E/(2*(dist_step**2)))*C.iloc[j+1,i-1])

print(C) #Some insanely large 0numbers 

"""Plot the upstream and downstream hydrographs on the same plot."""
"""
x=test["Time"]
fig, ax = plt.subplots()
ax.plot(test["Time"], test["Upstream"])
ax.plot(test["Time"], test["Downstream"])
plt.xlabel("Time (Day and Hour) - timestep = %i min" % time_min)	
fig.autofmt_xdate(bottom=None, rotation=30)
#ax.fmt_xdata = mdates.DateFormatter('%d')
plt.ylabel("Streamflow (in cfs)")
plt.title("Stream Routing of Lehigh River from Lake Cowichan to Duncan")
plt.legend()
plt.show()
"""
