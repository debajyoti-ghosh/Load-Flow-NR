import numpy as np

def calculate_for(BusList,YBus,Y_Pol):
    PV_Bus=PQ_Bus=0
    for Bus in BusList:    
        if Bus['Bus Code']==0:
            PQ_Bus +=1 
        elif Bus['Bus Code']==2:
            PV_Bus +=1
        else: Slack_Bus_Number = Bus['Bus No']
   

    J1 = np.zeros((PV_Bus+PQ_Bus, PV_Bus+PQ_Bus))
    J2 = np.zeros((PV_Bus+PQ_Bus, PV_Bus+PQ_Bus))
    J3 = np.zeros((PV_Bus+PQ_Bus, PV_Bus+PQ_Bus))
    J4 = np.zeros((PV_Bus+PQ_Bus, PV_Bus+PQ_Bus))

    ##formation of J1
    ##Creating diagonal elements
    i=0
    while i<(PV_Bus+PQ_Bus):
        for Bus_i in BusList:
            if Bus_i['Bus Code']!=1:
                for Bus_j in BusList:
                    if Bus_i['Bus No']!=Bus_j['Bus No']:
                        J1[i,i]+=Bus_i['V']*Bus_j['V']*Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r']*\
                            np.sin(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta']+Bus_j['delta']-Bus_i['delta'])
                i+=1

            
    ##Creating off-diagonal elements
    i=0
    for Bus_i in BusList:
        if Bus_i['Bus Code']!=1:
            j=0
            for Bus_j in BusList:
                if Bus_j['Bus Code']!=1:
                    if Bus_i['Bus No']!=Bus_j['Bus No']:
                        J1[i,j]=-1*Bus_i['V']*Bus_j['V']*Y_Pol[i+1][j+1]['r']*\
                            np.sin(Y_Pol[i+1][j+1]['theta']+Bus_j['delta']-Bus_i['delta'])
                        ##print(J1)
                    j+=1
            i+=1





   

    ##formation of J2
    ##Creating diagonal elements
    i=0
    for Bus_i in BusList:    
            if Bus_i['Bus Code']!=1 and i<(PV_Bus+PQ_Bus):
                for Bus_j in BusList:
                    if Bus_i['Bus No']!=Bus_j['Bus No']:
                        J2[i,i]+=Bus_j['V']*Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r']*\
                            np.cos(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta']+Bus_j['delta']-Bus_i['delta'])
                    else: J2[i,i]+=2*Bus_i['V']*Y_Pol[Bus_i['Bus No']-1][Bus_i['Bus No']-1]['r']*\
                            np.cos(Y_Pol[Bus_i['Bus No']-1][Bus_i['Bus No']-1]['theta'])
                i+=1

    ##Creating off-diagonal elements
    i=0
    for Bus_i in BusList:
        if Bus_i['Bus Code']!=1:
            j=0
            for Bus_j in BusList:
                if Bus_j['Bus Code']!=1:
                    if Bus_i['Bus No']!=Bus_j['Bus No'] :
                        J2[i,j]=Bus_i['V']*Y_Pol[i+1][j+1]['r']*\
                            np.cos(Y_Pol[i+1][j+1]['theta']+Bus_j['delta']-Bus_i['delta'])
                        ##print(J2)
                    j+=1
            i+=1




    


    ##formation of J3
    ##Creating diagonal elements
    i=0
    for Bus_i in BusList: 
            if Bus_i['Bus Code']!=1 and i<(PV_Bus+PQ_Bus):
                for Bus_j in BusList:
                    if Bus_i['Bus No']!=Bus_j['Bus No']:
                        J3[i,i]+=Bus_i['V']*Bus_j['V']*Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r']*\
                                np.cos(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta']+Bus_j['delta']-Bus_i['delta'])
                                                
                i+=1


    ##Creating off-diagonal elements
    i=0
    for Bus_i in BusList:
        #print(i)
        #print('B-i',Bus_i['Bus No'])
        if Bus_i['Bus Code']!=1:
            #print(i)
            #print('B-i',Bus_i['Bus No'])
            j=0
            for Bus_j in BusList:
                #print('i',i)
                #print('B-i',Bus_i['Bus No'])
                #print('j',j)
                #print('B-j',Bus_j['Bus No'])
                if Bus_j['Bus Code']!=1:
                    if Bus_i['Bus No']!=Bus_j['Bus No'] :
                        
                        J3[i,j]=-1*Bus_i['V']*Bus_j['V']*Y_Pol[i+1][j+1]['r']*\
                            np.cos(Y_Pol[i+1][j+1]['theta']+Bus_j['delta']-Bus_i['delta'])
                        
                        ##print(J3)
                    j+=1
            i+=1





   
   
   
    ##formation of J4
    ##Creating diagonal elements
    i=0
    for Bus_i in BusList:
            if Bus_i['Bus Code']!=1 and i<(PV_Bus+PQ_Bus):
                for Bus_j in BusList:
                    
                    if Bus_i['Bus No']!=Bus_j['Bus No']:
                        J4[i,i]-=Bus_j['V']*Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r']*\
                            np.sin(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta']+Bus_j['delta']-Bus_i['delta'])
                    else: J4[i,i]-=2*Bus_i['V']*Y_Pol[Bus_i['Bus No']-1][Bus_i['Bus No']-1]['r']*\
                            np.sin(Y_Pol[Bus_i['Bus No']-1][Bus_i['Bus No']-1]['theta'])
                    
                i+=1
   
   
    ##Creating off-diagonal elements
    i=0
    for Bus_i in BusList:
        if Bus_i['Bus Code']!=1:
            j=0
            for Bus_j in BusList:
                if Bus_j['Bus Code']!=1:
                    if Bus_i['Bus No']!=Bus_j['Bus No']:
                        
                        J4[i,j]=-1*Bus_i['V']*Y_Pol[i+1][j+1]['r']*\
                            np.sin(Y_Pol[i+1][j+1]['theta']+Bus_j['delta']-Bus_i['delta'])
                        
                        #print(J4)
                    j+=1
            i+=1
   
   
   
    J1J2 = np.concatenate((J1,J2), axis=1)
    J3J4 = np.concatenate((J3,J4), axis=1)
    J=np.concatenate((J1J2,J3J4), axis=0)
   
    i=0
    for Bus in BusList:
        i+=1
        if Bus['Bus Code']==2:
            for j in range (2*(PV_Bus+PQ_Bus)):
                if i+PV_Bus+PQ_Bus-2!=j:
                    J[i+PV_Bus+PQ_Bus-2][j]=0
                else:J[i+PV_Bus+PQ_Bus-2][j]=1


    print(J)
    
    return J