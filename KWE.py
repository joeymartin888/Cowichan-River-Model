import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.dates as mdates


def route(time_min, dist_ft, Length, cross, up, lat_flows):

    
    """Question 1: Route the streamflow from Walnutport to Whitehall, ensuring the 
    Courant condition is met."""
    
    #time_min=3 #Change timestep as required to meet Courant condition
    timestep=[]
    j=0
    while j<(60/time_min):
    	timestep.append(time_min*j)
    	j+=1
    
    #print (timestep)
    q=pd.DataFrame(0, index=range(len(up)*len(timestep)-(len(timestep)-1)), columns=["YEAR", "MONTH", "DAY", "HOUR","MINUTE","Upstream","Downstream"])
    for i in range(len(up)):
    	for t in range(len(timestep)):
    		q.iloc[(i*len(timestep)+t),0]=up.iloc[i,0]
    		q.iloc[(i*len(timestep)+t),1]=up.iloc[i,1]
    		q.iloc[(i*len(timestep)+t),2]=up.iloc[i,2]
    		q.iloc[(i*len(timestep)+t),3]=up.iloc[i,3]
    		q.iloc[(i*len(timestep)+t),4]=timestep[t]
    		if i==(len(up)-1):
    			q.iloc[(i*len(timestep)+t),5]=up.iloc[i,4]
    			break
    		q.iloc[(i*len(timestep)+t),5]=((up.iloc[i+1,4]-up.iloc[i,4])*t)/(len(timestep))+up.iloc[i,4]
    
    #print (q)
    
    #dist_ft=5280/4
    diststep=[]
    k=0
    while dist_ft*k<=Length:
    	diststep.append(dist_ft*k)
    	k+=1
    #print (diststep)

    
    qroute=pd.DataFrame(0, index=range(len(q)), columns=diststep)
    v_matrix=pd.DataFrame(0, index=range(len(q)), columns=diststep)
   
    lat_input=pd.DataFrame(0, index=[0], columns=diststep)
    
    for i in range(len(lat_flows)):
        for j in range (len(lat_input.columns.values)):
            if j==(len(lat_input.columns.values)-1) and (lat_flows[i,0] > lat_input.columns.values[j]):
                lat_input.iloc[0,j]=lat_flows[i,1] 
            elif (lat_flows[i,0] > lat_input.columns.values[j]) and (lat_flows[i,0] < lat_input.columns.values[j+1]):
                print(lat_input.columns.values[j])    
                lat_input.iloc[0,j]=lat_flows[i,1] 
                
    print(lat_input)
    
    qroute.iloc[0,:]=q.iloc[0,5] #set initial conditions
    qroute.iloc[:,0]=q.iloc[:,5]
    step=(time_min*60.0)/dist_ft
    #print(step)
    alpha=4.13 #temp
    beta=0.6 #confirm
    
    
    #print(qroute.iloc[1,0])
    #print(step+alpha*beta*((qroute.iloc[0,1]+qroute.iloc[1,0])/2)**(0.6-1))
    
    for j in range(len(q)-1):
        for i in range(len(diststep)-1):
            qroute.iloc[(j+1),(i+1)]=(step*qroute.iloc[(j+1),i]+alpha*beta*qroute.iloc[j,(i+1)]*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))/(step+alpha*beta*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))
            qroute.iloc[j+1,i+1]+=lat_input.iloc[0,i+1]
    
    
    v_matrix=qroute/cross
    
    newq=pd.DataFrame(columns=["Time", "Upstream","Downstream"])
    newq["Time"]=pd.to_datetime(q.iloc[:,0:5])
    newq["Upstream"]=q["Upstream"]
    newq["Downstream"]=qroute[Length]
    
    return newq
    #return v_matrix

#q["Whitehall"]=qroute.iloc[:,(len(qroute.columns)-1)]

