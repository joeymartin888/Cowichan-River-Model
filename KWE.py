import pandas as pd


def route(time_min, dist_step, length, width, slope, roughness, up, lat_flows):

    """Route the streamflow from Lake Cowichan to Duncan, ensuring the 
    Courant condition is met."""
    
    """Function will print the distance and time of the "bin" each inflow has been 
    assgined to if point lateral flows are turned on"""
    
    """
    inputs:
    
        time_min: the time step in minutes (decimals are functional)
    
    dist_step: the distance step (accepts either units)
    
    length: length of the river to be routed - units must match dist_step
    
    width: width of the river to be routed - units must match dist_step
    
    slope: slope of the river to be routed
    
    roughness: Manning coefficient for the river - standard default is 0.035
    
    up: a pd.Dataframe containing a column "Date" of pd.Timestamps and column "Value" of streamflows (m^3/s)
    main.py reformats ECCC historical hydrometric data to be compatible with this function
    
    lat_flows: a pd.Dataframe of point source inflows with three unlabelled columns:
        - distance downstream (int)
        - time of inflow (pd.Timestamp)
        - amount of inflow (m^3/s)
    
    
    outputs:
    
    KWE.route() returns a matrix of velocities for the defined time and distance steps of the river
    
    These is infrastructure within the code to return a modelled streamflow fro the purposes of validation
    
    """
    
    """Interpolates inputted data for the chosen time step"""
    start=up.iloc[0,0]
    end=up.iloc[(len(up)-1),0]
    x=up.set_index(pd.to_datetime(up["Date"]))
    del x["Date"]
    new_index = pd.date_range(start, end, freq=('%smin' % time_min))
    q=x.reindex(new_index).interpolate()
    print(q)
       
    """Defining an array of distance steps for the column labels"""
    diststep=[]
    k=0
    while dist_step*k<=length:
    	diststep.append(dist_step*k)
    	k+=1
        
    qroute=pd.DataFrame(0, index=q.index, columns=diststep)
    vroute=pd.DataFrame(0, index=q.index, columns=diststep) 
    lat_input=pd.DataFrame(0, index=q.index, columns=diststep)
    
    #Organizes inflows by time and distance 
    #Turned off to decrease computational time as no specific flows are being added or substracted
    #Crofton pulp mill outflow could be added here
    """for i in range(len(lat_flows)):
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
                        print(lat_input.index.values[k])"""
                            
    """Setting initial conditions"""
    qroute.iloc[0,:]=q.iloc[0,0] 
    vroute.iloc[0,:]=qroute.iloc[0,:]/(width*((roughness*qroute.iloc[0,0])/(1.49*(slope**0.5)*300))**0.6)
    qroute.iloc[:,0]=q.iloc[:,0]
    vroute.iloc[:,0]=q.iloc[:,0]/(width*((roughness*q.iloc[:,0])/(1.49*(slope**0.5)*300))**0.6)
    step=(time_min*60.0)/dist_step
        
    """Calculating alpha and beta"""
    beta=0.6
    alpha=((roughness*(width**(2.0/3.0)))/(1.49*(slope**0.5)))**beta
        
      
    """Routing of the River"""
    for j in range(len(q)-1):
        if (j%1000)==0: #progress metre
            print(((j*100.0)/len(q)))
        for i in range(len(diststep)-1):
            qroute.iloc[j+1,i+1]=(step*qroute.iloc[(j+1),i]+alpha*beta*qroute.iloc[j,(i+1)]*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))/(step+alpha*beta*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))
            qroute.iloc[j+1,i+1]+=lat_input.iloc[j+1,i+1] #Insert inflow
            if qroute.index[j+1].month==6:
                #if qroute.index[j+1].day==1:
                #    print("June")
                qroute.iloc[j+1,i+1]+=2.99321540575054/(len(diststep)*30*24*60*(60/time_min))
            if qroute.index[j+1].month==7:
                #if qroute.index[j+1].day==1:
                #    print("July")
                qroute.iloc[j+1,i+1]+=1.55594457215226/(len(diststep)*31*24*60*(60/time_min))
            if qroute.index[j+1].month==8:
                #if qroute.index[j+1].day==1:
                #    print("August")
                qroute.iloc[j+1,i+1]+=1.69157170192825/(len(diststep)*31*24*60*(60/time_min))
            if qroute.index[j+1].month==9:
                #if qroute.index[j+1].day==1:
                #    print("September")
                qroute.iloc[j+1,i+1]+=0.612205794127706/(len(diststep)*31*24*60*(60/time_min))
            flow_depth=((roughness*qroute.iloc[j+1,i+1])/(1.49*(slope**0.5)*300))**0.6
            #if j%100==0:
                #print(flow_depth)
            vroute.iloc[j+1,i+1]=qroute.iloc[j+1,i+1]/(flow_depth*width)
            #if j==1: 
             #   print(flow_depth)  #To check for flow depth for cross section
            celerity=((1.49*(slope**0.5))/(roughness))*(5.0/3.0)*(flow_depth**(2.0/3.0))
            if (time_min*60)>(dist_step/celerity): #Check Courant Condition
                print("Courant condition broken. delta x/Celerity = %f" % (dist_step/celerity))
                return
    
    """newq can be returned with the modelled downstream flow for the purposes of validation"""
    newq=pd.DataFrame(columns=["Time", "Upstream","Downstream"])
    newq["Time"]=q.index
    newq["Upstream"]=q.iloc[:,0]
    newq["Downstream"]=qroute[length]
    
    
    return vroute
    

