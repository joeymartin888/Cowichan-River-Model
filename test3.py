#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:43:08 2020

@authors: Joseph Martin, University of Victoria
Kelsey Shaw, University of Victoria
Andrew Freiburger, University of Victoria
"""
import pandas as pd
import KWE2 as KWE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.dates as mdates
import calendar

date_range=[pd.Timestamp('2012-06-01'), pd.Timestamp('2012-06-30')]
data=pd.read_csv("Lake_Cowichan_Historical_Daily.csv") #daily historical data
del data["PARAM"], data["SYM"], data[" ID"]
data["Date"]=pd.to_datetime(data["Date"])
data=data.where((data["Date"]>=date_range[0]) & (data["Date"] <= date_range[1])).dropna(axis=0)


data_down=pd.read_csv("Duncan_Historical_Daily.csv") #daily historical data
del data_down["PARAM"], data_down["SYM"], data_down[" ID"]
data_down["Date"]=pd.to_datetime(data_down["Date"])
data_down=data_down.where((data_down["Date"]>=date_range[0]) & (data_down["Date"] <= date_range[1])).dropna(axis=0)

C_month=pd.read_csv("Monthly_Nitrogen_Loading.csv")
time_min=0.5 #delta t
dist_step=3800 #delta x
length=38000+dist_step #River Length
width=25 #River Width
slope=0.005
roughness=0.035 #Manning’s roughness constant (this is Lehigh River value)'
decay_coeff=0.015 
E=7.5

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
"""Inflows can be put into the DataFrame in the format [distance along river, time 
(type Timestamp), Q_cfs]. Any number can be put in."""

#test=KWE.route(time_min, dist_step, length, width, slope, roughness, data, lat_flows) #returns the q route matrix


diststep=[]
k=0
while dist_step*k<=length:
	diststep.append(dist_step*k)
	k+=1
    
v_matrix=pd.DataFrame(0.003, index=dd.index, columns=diststep)

#v_matrix=test
#for col in v_matrix.columns:
    #v_matrix[col].values[:] = 0.49
print(v_matrix)

    
C_input=C=pd.DataFrame(0, index=v_matrix.index, columns=diststep)

ALR1=(436642617*1000/(width*dist_step*0.09))/(C_input.index.days_in_month*24*60*(60/time_min))
ALR2=(36767350*1000/(width*dist_step*0.09))/(C_input.index.days_in_month*24*60*(60/time_min))
ALR3=(5766103058*1000/(width*dist_step*0.09))/(C_input.index.days_in_month*24*60*(60/time_min))
C_flows=pd.DataFrame([[750,ALR1],[25750,ALR2],[32500,ALR3]])

#print(C_month["ALR1"].where(C_month["Month"]==C_input.index[0].month).mean())


for i in range(len(C_flows)):
        for j in range (len(C_input.columns.values)):
            if j==(len(C_input.columns.values)-1) and (C_flows.iloc[i,0] >= C_input.columns.values[j]):
                C_input.iloc[:,j]=C_flows.iloc[i,1]
            elif (C_flows.iloc[i,0] >= C_input.columns.values[j]) and (C_flows.iloc[i,0] < C_input.columns.values[j+1]):
                C_input.iloc[:,j]=C_flows.iloc[i,1]

print(C_input)
  
C=pd.DataFrame(0, index=v_matrix.index, columns=diststep)
C.insert(loc=0, column='Initial', value=0.033)
#C.iloc[0,0]=100
print("here")

for j in range(len(v_matrix)-1):
    if (j%1000)==0: #progress metre
        print(((j*100.0)/len(v_matrix)))
    for i in range(1,(len(diststep)-1)):
        b1=(time_min*60)*(1.0/(time_min*60)-(2.0*E)/(dist_step**2)-decay_coeff)
        b2=(time_min*60)*((-v_matrix.iloc[j,i])/(2*dist_step)+E/(dist_step**2))
        b3=(time_min*60)*((v_matrix.iloc[j,i])/(2*dist_step)+E/(dist_step**2))
        s1=((time_min*60*v_matrix.iloc[j,i])/dist_step)**2
        s2=(2*E*time_min*60)/(dist_step**2)
        if (s1<0):
            print("Unstable, (Ut/x)^2=%f" % s1)
        if (s1>s2):
            print("Unstable, (Ut/x)^2=%f 2Et/(x^2)=%f" % (s1,s2))
        if (s2>1):
            print("Unstable, 2Et/(x^2)=%f" % s2)
        if i==0:
             C.iloc[j+1,i]=b1*C.iloc[j,i]+b2*C.iloc[j,i+1] #because C_x-1=0
             if C.iloc[j+1,i]<0:
                 print("%.4f, %.4f" % (b1, b2))
             C.iloc[j+1,i]=(C.iloc[j+1,i]*(width*dist_step*0.09)+C_input.iloc[j+1,i])/(width*dist_step*0.09)
        else:
            C.iloc[j+1,i]=b1*C.iloc[j,i]+b2*C.iloc[j,i+1]+b3*C.iloc[j,i-1]
            C.iloc[j+1,i]=(C.iloc[j+1,i]*(width*dist_step*0.09)+C_input.iloc[j+1,i])/(width*dist_step*0.09)
        if i==len(diststep)-3:
            #print(C.iloc[j+1,i])
            C.iloc[j+1,i+2]=C.iloc[j+1,i] #providing extra column for C_(x=N)

del C[length]            
print(C) #Negative numbers and (some?) conservation of mass...

#%%"""

"""Plot the upstream and downstream hydrographs on the same plot."""



"""ACC=np.corrcoef(dd["Value"],test[(length-dist_step)])[1,0]
print(ACC)"""

x=C.index
fig, ax = plt.subplots()
ax.plot(C.index, C[0], label="Upstream")
ax.plot(C.index, C[(length-dist_step)], label="Downstream")
plt.xlabel("Time (Day and Hour) - timestep = %.2f min" % time_min)	
fig.autofmt_xdate(bottom=None, rotation=30)
#ax.fmt_xdata = mdates.DateFormatter('%d')
plt.ylabel("Concentration (mg/L)")
plt.title("Nitrate Concentrations at Lake Cowichan and Duncan from %s 01-02 %s" % ((calendar.month_name[start.month]), end.year))
plt.legend()
plt.show()


#print("Integral of Upstream = %.3f" % sum(C[0]))
#print("Integral of Downstream = %.3f" % sum(C[(length-dist_step)]))

#print(v_matrix.index.month.mean())

#C_month['Month'] = pd.to_datetime(C_month['Month'], format='%m')


#print(C_month["ALR1"].where(C_month["Month"]==v_matrix.index.month.mean()))
#C_month["Month"]=C_month["Month"].to_datetime


                    

