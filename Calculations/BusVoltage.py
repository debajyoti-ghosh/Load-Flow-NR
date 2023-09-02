import numpy as np
def calculate_for(BusList,del_PQ,JacobMatrix):
    Solved_BusVolt_List=[]
    print(JacobMatrix)
    Jacob_INV= np.linalg.inv(JacobMatrix)
    length=len(del_PQ)
    only_del_PQ=np.zeros([length,1])
    for i in range(length):
        only_del_PQ[i][0]=del_PQ[i]['del']
    
    print(Jacob_INV)
    print(only_del_PQ)
    del_Volt = Jacob_INV.dot(only_del_PQ)
    print(del_Volt)
    print('delV',del_Volt)
    for i in range(length):
        for Bus in BusList:
            #print(del_PQ[i]['Bus No'])
            #print(Bus['Bus No'])
            if del_PQ[i]['Bus No']== Bus['Bus No'] :
                if del_PQ[i]['Type']=='P':
                    #print(del_Volt[i].item())
                    Bus['delta']+=del_Volt[i].item()
                    #print(Bus['delta'])
                elif del_PQ[i]['Type']=='Q':
                   # print(del_Volt[i].item())
                    Bus['V']+=del_Volt[i].item()
                   # print(Bus['V'])
    
    for Bus in BusList:
        l = ['Bus No','Bus Code','V','delta']
        #Solved_BusVolt={key: Bus[key] for key in Bus.keys() & l} 
        Solved_BusVolt={i:Bus[i] for i in l} ## Slicing Dic
        Solved_BusVolt_List.append(Solved_BusVolt)
       # print(Solved_BusVolt_List)
    print(Solved_BusVolt_List)
    return Solved_BusVolt_List,BusList
            