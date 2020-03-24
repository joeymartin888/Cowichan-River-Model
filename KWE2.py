import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.dates as mdates


def route(time_min, dist_ft, Length, width, slope, roughness, up, lat_flows):

    """Route the streamflow from Lake Cowichan to Duncan, ensuring the 
    Courant condition is met."""
    
    """Function will print the distance and time of the "bin" each inflow has been 
    assgined to."""
    
    """timestep=[]
    j=0
    while j<(60/time_min):
    	timestep.append(time_min*j)
    	j+=1"""
    
    """#Adds time steps in minutes as the input data only works in hours.
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
    """
    start=up.iloc[0,0]

    end=up.iloc[(len(up)-1),0]

    x=up.set_index(pd.date_range(start,end, freq='5min'))
    del x[u'Date (PST)']
    del x[u'Parameter ']
    new_index = pd.date_range(start, end, freq=('%smin' % time_min))
    
    

    q=x.reindex(new_index).interpolate()
    
       
    diststep=[]
    k=0
    while dist_ft*k<=Length:
    	diststep.append(dist_ft*k)
    	k+=1
    #print (diststep)
    
    qroute=pd.DataFrame(0, index=q.index, columns=diststep)
     
 
    lat_input=pd.DataFrame(0, index=q.index, columns=diststep)
    
    #Organizes inflows by time and distance
    for i in range(len(lat_flows)):
        for j in range (len(lat_input.columns.values)):
            for k in range(len(lat_input)):
                if j==(len(lat_input.columns.values)-1) and (lat_flows.iloc[i,0] >= lat_input.columns.values[j]):
                    if k==(len(lat_input)-1) and (lat_flows.iloc[i,1] >= lat_input.index.values[k]):
                        lat_input.iloc[k,j]=lat_flows.iloc[i,2]
                    elif (lat_flows.iloc[i,1] >= lat_input.index.values[k]) and (lat_flows.iloc[i,1] < lat_input.index.values[k+1]):
                        lat_input.iloc[k,j]=lat_flows.iloc[i,2]
                elif (lat_flows.iloc[i,0] >= lat_input.columns.values[j]) and (lat_flows.iloc[i,0] < lat_input.columns.values[j+1]):
                    if k==(len(lat_input)-1) and (lat_flows.iloc[i,1] >= lat_input.index.values[k]):
                        lat_input.iloc[k,j]=lat_flows.iloc[i,2]
                    elif (lat_flows.iloc[i,1] >= lat_input.index.values[k]) and (lat_flows.iloc[i,1] < lat_input.index.values[k+1]):
                        lat_input.iloc[k,j]=lat_flows.iloc[i,2]
                        print(lat_input.columns.values[j])
                        print(lat_input.index.values[k])
                            
          
    #print(lat_input)
    
    qroute.iloc[0,:]=q.iloc[0,0] #set initial conditions
    qroute.iloc[:,0]=q.iloc[:,0]
    step=(time_min*60.0)/dist_ft
    #print(step)
    beta=0.6 #confirm
    alpha=((roughness*(width**(2.0/3.0)))/(1.49*(slope**0.5)))**beta #temp
    print(alpha)
    
    
    #print(qroute.iloc[1,0])
    #print(step+alpha*beta*((qroute.iloc[0,1]+qroute.iloc[1,0])/2)**(0.6-1))
    
    #Acutal routing of the stream
    for j in range(len(q)-1):
        for i in range(len(diststep)-1):
            qroute.iloc[(j+1),(i+1)]=(step*qroute.iloc[(j+1),i]+alpha*beta*qroute.iloc[j,(i+1)]*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))/(step+alpha*beta*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))
            qroute.iloc[j+1,i+1]+=lat_input.iloc[j+1,i+1] #Insert inflow
            flow_depth=((roughness*qroute.iloc[j+1,i+1])/(1.49*(slope**0.5)*300))**0.6
            #if j==1: 
             #   print(flow_depth)  #To check for flow depth for cross section
            celerity=((1.49*(slope**0.5))/(roughness))*(5.0/3.0)*(flow_depth**(2.0/3.0))
            if (time_min*60)>(dist_ft/celerity): #Check Courant Condition
                print("Courant condition broken. delta x/Celerity = %f" % (dist_ft/celerity))
                return
    
    
    #print(qroute/(width*flow_depth))
    

    newq=pd.DataFrame(columns=["Time", "Upstream","Downstream"])
    newq["Time"]=q.index
    newq["Upstream"]=q.iloc[:,0]
    newq["Downstream"]=qroute[Length]
    
    #return newq
    return qroute
    #return v_matrix

#q["Whitehall"]=qroute.iloc[:,(len(qroute.columns)-1)]

