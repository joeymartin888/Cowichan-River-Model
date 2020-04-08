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
    
    length=v_matrix.columns[(len(v_matrix.columns)-1)]
    
    diststep=[]
    k=0
    while dist_step*k<=length:
    	diststep.append(dist_step*k)
    	k+=1
        
    C_input=C=pd.DataFrame(0, index=v_matrix.index, columns=diststep)

    ALR1=(436642617*1000/(width*dist_step*flow_depth))/(C_input.index.days_in_month*24*60*(60/time_min))
    ALR2=(36767350*1000/(width*dist_step*flow_depth))/(C_input.index.days_in_month*24*60*(60/time_min))
    ALR3=(5766103058*1000/(width*dist_step*flow_depth))/(C_input.index.days_in_month*24*60*(60/time_min))
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
            b1=(time_min*60)*(1.0/(time_min*60)-(2.0*disp_coeff)/(dist_step**2)-decay_coeff)
            b2=(time_min*60)*((-v_matrix.iloc[j,i])/(2*dist_step)+disp_coeff/(dist_step**2))
            b3=(time_min*60)*((v_matrix.iloc[j,i])/(2*dist_step)+disp_coeff/(dist_step**2))
            s1=((time_min*60*v_matrix.iloc[j,i])/dist_step)**2
            s2=(2*disp_coeff*time_min*60)/(dist_step**2)
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
                 C.iloc[j+1,i]=(C.iloc[j+1,i]*(1/1000.0)*(width*dist_step*flow_depth)+C_input.iloc[j+1,i])/(width*dist_step*flow_depth/1000)
            else:
                C.iloc[j+1,i]=b1*C.iloc[j,i]+b2*C.iloc[j,i+1]+b3*C.iloc[j,i-1]
                C.iloc[j+1,i]=(C.iloc[j+1,i]*(1/1000.0)*(width*dist_step*flow_depth)+C_input.iloc[j+1,i])/(width*dist_step*flow_depth/1000)
            if i==len(diststep)-3:
                #print(C.iloc[j+1,i])
                C.iloc[j+1,i+2]=C.iloc[j+1,i] #providing extra column for C_(x=N)

    del C[length]            
    return C 
