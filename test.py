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
dist_step_min=5280 #delta x
slope=0.005
roughness=0.025 #Manning’s roughness constant (this is Lehigh River value)

lat_flows=pd.DataFrame([[8000,pd.Timestamp('2008-03-06T07'),10000],[10000,pd.Timestamp('2008-03-05T06'),3000],[52000,pd.Timestamp('2008-03-06T09'),20000]]) #[distance on the river, flow]
"""Inflows can be put into the DataFrame in the format [distance along river, time 
(type Timestamp), Q_cfs]. Any number can be put in."""

test=KWE.route(time_min, dist_step_min, length, width, slope, roughness, data, lat_flows)

print(test)

"""Plot the upstream and downstream hydrographs on the same plot."""

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

