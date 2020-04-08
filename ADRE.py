#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:50:00 2020

@authors: Joseph Martin, University of Victoria
Kelsey Shaw, University of Victoria
Andrew Freiburger, University of Victoria
"""

import pandas as pd

def route(time_min, dist_step, width, flow_depth, v_matrix, disp_coeff, decay_coeff):
    
    """Model the concentration of nitrates from Lake Cowichan to Duncan, ensuring the 
    Fletcher (1990) conditions are met."""
    
    """The nitrate loading is currently defined within this function as constants.
    In future, it may be worth implementing this as point source inputs similar to
    the lateral flows for the KWE function."""
    
    """
    inputs:
    
    time_min: the time step in minutes (decimals are functional)
    
    dist_step: the distance step (accepts either units)
    
    width: width of the river to be routed - units must match dist_step
    
    slope: slope of the river to be routed
    
    v_matrix: produced by KWE function - a matrix of velocities (m/s) for the defined time and 
    distance steps of the river
    
    disp_coeff: dispersion coefficient from the literaure (m^2/s)
        
    decay_coeff: the rate of decay of nitrates from the literature (day^-1)
    
  
    outputs:
    
    ADRE.route() returns a matrix of concentrations (mg/L) for the defined time and distance steps of the river
    """
    
    """Copy length and column labels from v_matrix"""
    length=v_matrix.columns[(len(v_matrix.columns)-1)] 
    diststep=v_matrix.columns
        
    C_input=C=pd.DataFrame(0, index=v_matrix.index, columns=diststep)
    
    """Constant nitrate inputs for three ALRs along the Cowichan River concentrations are mg/L taken 
    from mg per month for each ALR into the volume of the distance step"""
    ALR1=(436642617*1000/(width*dist_step*flow_depth))/(C_input.index.days_in_month*24*60*(60/time_min))
    ALR2=(36767350*1000/(width*dist_step*flow_depth))/(C_input.index.days_in_month*24*60*(60/time_min))
    ALR3=(5766103058*1000/(width*dist_step*flow_depth))/(C_input.index.days_in_month*24*60*(60/time_min))
    
    C_flows=pd.DataFrame([[750,ALR1],[25750,ALR2],[32500,ALR3]]) #Lengths and ALR values could be inputs vice defined inside the function

    """Organizing nitrate loading by distance step"""
    for i in range(len(C_flows)):
        for j in range (len(C_input.columns.values)):
            if j==(len(C_input.columns.values)-1) and (C_flows.iloc[i,0] >= C_input.columns.values[j]):
                C_input.iloc[:,j]=C_flows.iloc[i,1]
            elif (C_flows.iloc[i,0] >= C_input.columns.values[j]) and (C_flows.iloc[i,0] < C_input.columns.values[j+1]):
                C_input.iloc[:,j]=C_flows.iloc[i,1]
    
    C=pd.DataFrame(0, index=v_matrix.index, columns=diststep)
    C.insert(loc=0, column='Initial', value=0.033)

    """Advection, Dispersion, and Reaction calculations of nitrate concentrations"""
    for j in range(len(v_matrix)-1):
        if (j%1000)==0: #progress metre
            print(((j*100.0)/len(v_matrix)))
        for i in range(1,(len(diststep)-1)):
            b1=(time_min*60)*(1.0/(time_min*60)-(2.0*disp_coeff)/(dist_step**2)-decay_coeff)
            b2=(time_min*60)*((-v_matrix.iloc[j,i])/(2*dist_step)+disp_coeff/(dist_step**2))
            b3=(time_min*60)*((v_matrix.iloc[j,i])/(2*dist_step)+disp_coeff/(dist_step**2))
            s1=((time_min*60*v_matrix.iloc[j,i])/dist_step)**2
            s2=(2*disp_coeff*time_min*60)/(dist_step**2)
            
            """Ensure conditions of stability are met"""
            if (s1<0):
                print("Unstable, (Ut/x)^2=%f" % s1)
            if (s1>s2):
                print("Unstable, (Ut/x)^2=%f 2Et/(x^2)=%f" % (s1,s2))
            if (s2>1):
                print("Unstable, 2Et/(x^2)=%f" % s2)
            
            """If initial conditions are defined as zero, this block avoids having
            to define an initial column - not implemented for Cowichan River Model"""
            if i==0:
                 C.iloc[j+1,i]=b1*C.iloc[j,i]+b2*C.iloc[j,i+1] #because C_x-1=0
                 if C.iloc[j+1,i]<0:
                     print("%.4f, %.4f" % (b1, b2))
                 C.iloc[j+1,i]=(C.iloc[j+1,i]*(1/1000.0)*(width*dist_step*flow_depth)+C_input.iloc[j+1,i])/(width*dist_step*flow_depth/1000)
            
            else:
                C.iloc[j+1,i]=b1*C.iloc[j,i]+b2*C.iloc[j,i+1]+b3*C.iloc[j,i-1]
                C.iloc[j+1,i]=(C.iloc[j+1,i]*(1/1000.0)*(width*dist_step*flow_depth)+C_input.iloc[j+1,i])/(width*dist_step*flow_depth/1000)
            
            """This block inserts an copy of the second last column after the last column
            as is required for thr FTCS numerical method"""
            if i==len(diststep)-3:
                #print(C.iloc[j+1,i])
                C.iloc[j+1,i+2]=C.iloc[j+1,i] #providing extra column for C_(x=N)

    del C[length] #removes the extra column for FTCS       
    
    return C 
