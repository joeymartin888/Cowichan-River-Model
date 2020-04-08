#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:43:08 2020

@author: Joseph Martin, University of Victoria
"""
import pandas as pd
import KWE2 as KWE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.dates as mdates

data=pd.read_csv("08HA002_QR_Mar-23-2020_08_24_37PM.csv") #5 minute data
length=38000 #River Length
width=25 #River Width
time_min=3 #delta t
dist_step=3800/10 #delta x
slope=0.005
roughness=0.035 #Manning’s roughness constant (this is Lehigh River value)'
decay_coeff=0.015
E=7.5

lat_flows=pd.DataFrame([[8000,pd.Timestamp('2020-03-17T07'),0],[25000,pd.Timestamp('2020-03-20T06'),0],[32000,pd.Timestamp('2020-03-18T09'),0]])
"""Inflows can be put into the DataFrame in the format [distance along river, time 
(type Timestamp), Q_cfs]. Any number can be put in."""

test=KWE.route(time_min, dist_step, length, width, slope, roughness, data, lat_flows) #returns the q route matrix


v_matrix=test/(0.15*width) # 6-9 m/s
#print(v_matrix)

diststep=[]
k=0
while dist_step*k<=length:
	diststep.append(dist_step*k)
	k+=1
    
C=pd.DataFrame(0, index=test.index, columns=diststep)
C.iloc[:,0]=0.01

for j in range(len(v_matrix)-1):
        for i in range(len(diststep)-1):
            w1=(1.0/(2.0*time_min*60))-(v_matrix.iloc[j,i]/(2.0*dist_step))-(E/(dist_step**2.0))-(decay_coeff/4.0)
            w2=(1.0/(2.0*time_min*60))-(v_matrix.iloc[j,i+1]/(2.0*dist_step))+(E/(2.0*(dist_step**2.0)))-(decay_coeff/4.0)
            w3=(-1.0/(2.0*time_min*60))-(v_matrix.iloc[j+1,i]/(2.0*dist_step))-(E/(dist_step**2.0))-(decay_coeff/4.0)
            w4=(-1.0/(2.0*time_min*60))-(v_matrix.iloc[j+1,i+1]/(2.0*dist_step))+(E/(2*(dist_step**2.0)))-(decay_coeff/4.0)
            Cou=(v_matrix.iloc[j,i]*time_min*60)/dist_step
            if (Cou>1):
                print("Unstable, Cou=%f" % Cou)
            Pe=(v_matrix.iloc[j,i]*dist_step)/E
            if (Pe>2):
                print("Unstable, Pe=%f" % Pe)
            Dif=(E*time_min*60)/(dist_step**2)
            if (Dif>0.2):
                print("Unstable, Dif=%f" % Dif)
            if i==0:
                 C.iloc[j+1,i+1]=(-1.0/w4)*(w1*C.iloc[j,i]+w2*C.iloc[j,i+1]+w3*C.iloc[j+1,i]) #because C_x-1=0
            else:
                C.iloc[j+1,i+1]=(-1.0/w4)*(w1*C.iloc[j,i]+w2*C.iloc[j,i+1]+w3*C.iloc[j+1,i]+(E/(2*(dist_step**2)))*C.iloc[j,i-1]+(E/(2*(dist_step**2)))*C.iloc[j+1,i-1])
            
            
print(C) #Negative numbers and (some?) conservation of mass...

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
