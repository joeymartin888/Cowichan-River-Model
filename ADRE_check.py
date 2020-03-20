#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:09:32 2020

@author: Andrew Freiburger, University of Victoria
with contributions from Joseph Martin, University of Victoria
"""

#distance-step

#input parameters

#D units [1 per second]
D = input ("D value")
D_num = float(D)

#V units [meters per second]
V = input ("Maximum velocity")
V_num = float(V)

#distance units [meters]
dist_step = input("Distance step")
dist_step_num = float(dist_step)

#Evaluation of the distance-step
def distance(dist_step):
    if (dist_step > ((2*D_num)/V_num)):
        return str("Distance step is too great")
    else:
        return str("Distance step is acceptable")

#Td time-step

#input parameters

# k units [1 per second]
k = input("k value")
k_num = float(k)

#Determination of the individual time-step parameters
Td = ((dist_step_num**2)/D_num)
Tk = (1/k_num)
Tv = (dist_step_num/V_num)

#Evaluation of the time-step
lowest_parameter = min(Td,Tk,Tv)
def lowest(lowest_parameter):
    if (lowest_parameter > (2*dist_step)):
        return str("Time step is too great")
    else:
        return str("Time step is acceptable")
lowest(lowest_parameter)
