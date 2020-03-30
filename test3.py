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
C_month=pd.read_csv("Monthly_Nitrogen_Loading.csv")#, parse_dates=["Month"])
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

v_matrix=test
#v_matrix=test/(0.15*width*1000) # 6-9 m/s #artificially lowered
#for col in v_matrix.columns:
 #   v_matrix[col].values[:] = 0.49
print(v_matrix)

diststep=[]
k=0
while dist_step*k<=length:
	diststep.append(dist_step*k)
	k+=1
    
C_input=C=pd.DataFrame(0, index=v_matrix.index, columns=diststep)

ALR1=(C_month["ALR1"].where(C_month["Month"]==C_input.index[0].month).mean())/(C_input.index.days_in_month*24*(60/time_min))
ALR2=(C_month["ALR2"].where(C_month["Month"]==C_input.index[0].month).mean())/(C_input.index.days_in_month*24*(60/time_min))
ALR3=(C_month["ALR3"].where(C_month["Month"]==C_input.index[0].month).mean())/(C_input.index.days_in_month*24*(60/time_min))
C_flows=pd.DataFrame([[8000,ALR1],[25000,ALR2],[36000,ALR3]])

#print(C_month["ALR1"].where(C_month["Month"]==C_input.index[0].month).mean())


for i in range(len(C_flows)):
        for j in range (len(C_input.columns.values)):
            if j==(len(C_input.columns.values)-1) and (C_flows.iloc[i,0] >= C_input.columns.values[j]):
                C_input.iloc[:,j]=C_flows.iloc[i,1]
            elif (C_flows.iloc[i,0] >= C_input.columns.values[j]) and (C_flows.iloc[i,0] < C_input.columns.values[j+1]):
                C_input.iloc[:,j]=C_flows.iloc[i,1]
    
C=pd.DataFrame(0, index=v_matrix.index, columns=diststep)
#C.iloc[0,0]=0.01

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
                 C.iloc[j+1,i]+=C_input.iloc[j+1,i]
            else:
                C.iloc[j+1,i]=b1*C.iloc[j,i]+b2*C.iloc[j,i+1]+b3*C.iloc[j,i-1]
                C.iloc[j+1,i]+=C_input.iloc[j+1,i]
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

#%%



#print(v_matrix.index.month.mean())

#C_month['Month'] = pd.to_datetime(C_month['Month'], format='%m')


#print(C_month["ALR1"].where(C_month["Month"]==v_matrix.index.month.mean()))
#C_month["Month"]=C_month["Month"].to_datetime


                    

