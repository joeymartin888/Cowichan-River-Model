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

data=pd.read_csv("08HA002_QR_Mar-27-2020_07_14_05PM.csv") #5 minute data
time_min=0.5 #delta t
dist_step=3800 #delta x
length=38000+dist_step #River Length
width=25 #River Width
slope=0.005
roughness=0.035 #Manning’s roughness constant (this is Lehigh River value)'
decay_coeff=0 #To test tracer
E=7.5

print(data)
#%%
lat_flows=pd.DataFrame([[8000,pd.Timestamp('2020-03-17T07'),0],[25000,pd.Timestamp('2020-03-20T06'),0],[32000,pd.Timestamp('2020-03-18T09'),0]])
"""Inflows can be put into the DataFrame in the format [distance along river, time 
(type Timestamp), Q_cfs]. Any number can be put in."""

test=KWE.route(time_min, dist_step, length, width, slope, roughness, data, lat_flows) #returns the q route matrix

v_matrix=test/(0.15*width*1000) # 6-9 m/s #artificially lowered
#for col in v_matrix.columns:
 #   v_matrix[col].values[:] = 0.49
print(v_matrix)

diststep=[]
k=0
while dist_step*k<=length:
	diststep.append(dist_step*k)
	k+=1
    
C=pd.DataFrame(0, index=v_matrix.index, columns=diststep)
C.iloc[0,0]=0.01

for j in range(len(v_matrix)-1):
        for i in range(len(diststep)-1):
            b1=(time_min*60)*(1.0/(time_min*60)-(2.0*E)/(dist_step**2)-decay_coeff)
            b2=(time_min*60)*((-v_matrix.iloc[j,i])/(2*dist_step)+E/(dist_step**2))
            b3=(time_min*60)*((v_matrix.iloc[j,i])/(2*dist_step)+E/(dist_step**2))
            s1=((time_min*60*v_matrix.iloc[j,i])/dist_step)**2
            s2=(2*E*time_min*60)/(dist_step**2)
            if (s1<0):
                print("Unstable, Ut/x=%f" % s1)
            if (s1>s2):
                print("Unstable, Ut/x=%f 2Et/(x^2)=%f" % (s1,s2))
            if (s2>1):
                print("Unstable, 2Et/(x^2)=%f" % s2)
            if i==0:
                 C.iloc[j+1,i]=b1*C.iloc[j,i]+b2*C.iloc[j,i+1] #because C_x-1=0
                 #C.iloc[j+1,i]+=0.01
            else:
                C.iloc[j+1,i]=b1*C.iloc[j,i]+b2*C.iloc[j,i+1]+b3*C.iloc[j,i-1]
            if i==len(diststep)-3:
                #print(C.iloc[j+1,i])
                C.iloc[j+1,i+2]=C.iloc[j+1,i] #providing extra column for C_(x=N)

del C[length]            
print(C) #Negative numbers and (some?) conservation of mass...

#%%

"""Plot the upstream and downstream hydrographs on the same plot."""

x=C.index
fig, ax = plt.subplots()
ax.plot(C.index, C[0])
ax.plot(C.index, C[(length-dist_step)])
plt.xlabel("Time (Day and Hour) - timestep = %.2f min" % time_min)	
fig.autofmt_xdate(bottom=None, rotation=30)
#ax.fmt_xdata = mdates.DateFormatter('%d')
plt.ylabel("Concentration (in mg/L)")
plt.title("Nitrate Concentration in the Cowichan River from Lake Cowichan to Duncan")
plt.legend()
plt.show()

