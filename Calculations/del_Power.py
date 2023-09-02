import pandas
import numpy as np
# def calculate_for(BusList,Y_Pol):
#     ##Formation of del_Pi[]
#     Pi_List = []
#     for Bus_i in BusList:
#         if Bus_i['Bus Code']!=1:
#             Pi={'Bus No':Bus_i['Bus No'],'Value_Cal':0,'Value_Sch':Bus_i['P_Gen(pu)']-Bus_i['P_Load(pu)'],'del':0}
#             for Bus_j in BusList:
#                 Pi['Value_Cal']+=Bus_i['V']*Bus_j['V']*Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r']*\
#                     np.cos(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta']+Bus_j['delta']-Bus_i['delta'])            
#             Pi['del']=Pi['Value_Sch']-Pi['Value_Cal']
#             Pi_List.append(Pi['del'])
            

#     ##print(Pi_List)

#     ##Formation of del_Qi[]
#     Qi_List = []
#     for Bus_i in BusList:
#         if Bus_i['Bus Code']!=1 and Bus_i['Bus Code']!=2:
#             Qi={'Bus No':Bus_i['Bus No'],'Value_Cal':0,'Value_Sch':Bus_i['Q_Gen(pu)']-Bus_i['Q_Load(pu)'],'del':0}
#             for Bus_j in BusList:
#                 Qi['Value_Cal']-=Bus_i['V']*Bus_j['V']*Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r']*\
#                     np.sin(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta']+Bus_j['delta']-Bus_i['delta'])            
#             Qi['del']=Qi['Value_Sch']-Qi['Value_Cal']
#             Qi_List.append(Qi['del'])
            

#    # #print(Qi_List)
#     Pi_List = np.array(Pi_List).reshape((-1, 1))
#     Qi_List = np.array(Qi_List).reshape((-1, 1))
#     del_PQ=np.concatenate((Pi_List,Qi_List), axis=0)
#     return del_PQ






def calculate_for(BusList,Y_Pol):
    #print(BusList)
    ##Formation of del_Pi[]
    Pi_List = []
    for Bus_i in BusList:
        if Bus_i['Bus Code']!=1:
            Pi={'Type':'P','Bus No':Bus_i['Bus No'],'Value_Cal':0,'Value_Sch':Bus_i['P_Gen(pu)']-Bus_i['P_Load(pu)'],'del':0}
            print('Bi',Bus_i['Bus No'])
            for Bus_j in BusList:
                #print('Bj',Bus_j['Bus No'])
                #print(Bus_i['V'])
                #print(Bus_j['V'])
                #print(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r'])
                #print(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta'])
                #print(Bus_j['delta'])
                #print(Bus_i['delta'])

                Pi['Value_Cal']+=Bus_i['V']*Bus_j['V']*Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r']*\
                    np.cos(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta']+Bus_j['delta']-Bus_i['delta'])

                #print(Pi['Value_Cal'])            
            print(Pi['Value_Sch'])
            print(Pi['Value_Cal'])
            Pi['del']=Pi['Value_Sch']-Pi['Value_Cal']
            ##All values of Pi not required in future, also only del will make difficult to map in BusList
            l = {'Type', 'Bus No','Value_Sch','Value_Cal','del'}
            Pi={key: Pi[key] for key in Pi.keys() & l} ## Slicing Dic
            Pi_List.append(Pi)
            

    ##print(Pi_List)

    ##Formation of del_Qi[]
    Qi_List = []
    for Bus_i in BusList:
        if Bus_i['Bus Code']!=1:
            Qi={'Type':'Q','Bus No':Bus_i['Bus No'],'Value_Cal':0,'Value_Sch':Bus_i['Q_Gen(pu)']-Bus_i['Q_Load(pu)'],'del':0}
            for Bus_j in BusList:
                Qi['Value_Cal']-=Bus_i['V']*Bus_j['V']*Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['r']*\
                    np.sin(Y_Pol[Bus_i['Bus No']-1][Bus_j['Bus No']-1]['theta']+Bus_j['delta']-Bus_i['delta'])            
            if Bus_i['Bus Code']!=2:
                Qi['del']=Qi['Value_Sch']-Qi['Value_Cal']
            else: Qi['del']=0
            ##All values of Qi not required in future, also only del will make difficult to map in BusList
            l = {'Type', 'Bus No','Value_Sch','Value_Cal','del'}
            Qi={key: Qi[key] for key in Qi.keys() & l} ## Slicing Dic
            Qi_List.append(Qi)
            

   
    del_PQ=np.concatenate((Pi_List,Qi_List), axis=0)
    df = pandas.DataFrame(del_PQ)
    #df.to_excel('Gen Mismatch.xlsx',header=True)
    print(del_PQ)
    return del_PQ