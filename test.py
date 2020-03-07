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

data=pd.read_csv("River_routing_data.csv")
length=5280*10
cross=30*10
time_min=3
dist_step_min=5280/4

lat_flows=np.matrix([[4000,0],[500,0],[52000,10000]])

test=KWE.route(time_min, dist_step_min, length, cross, data, lat_flows)

print(test)

"""Question 2: Plot the upstream and downstream hydrographs on the same plot."""

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

"""Question 3: What is the speed of the flood wave? You may approximate
this with the time between the two peaks of the hydrographs."""
"""
flood_up=newq["Time"].where(newq["Walnutport"]==max(newq["Walnutport"]))
flood_down=newq["Time"].where(newq["Whitehall"]==max(newq["Whitehall"]))
f=flood_down.dropna()
g=flood_up.dropna()
flood_time=f.iloc[0]-g.iloc[0]
j=flood_time.seconds
flood_speed=Length/flood_time.seconds
print("The flood wave travelled at %0.2f cfs." % flood_speed)  """