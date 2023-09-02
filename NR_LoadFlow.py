import numpy as np
import pandas 
import json
import openpyxl
from Calculations import *
from Parameter import YBus

# ******************************* Input *******************************
# *********************************************************************

## Specify the input Data File 
DataFile = 'IEEE 30 Bus System.xlsx'
BusData_SheetName = 'BusData'
LineData_SheetName = 'LineData'

##Specify max number of iteration tolerance
max_iter=100
tollerance=0.00025
Sbase=100


# ********************************************************************



# *************************** Reading Data ****************************
# *********************************************************************

##Read Line Data
LineList = []
excel_linedata_df = pandas.read_excel(DataFile, sheet_name=LineData_SheetName)
Lines_json_str = excel_linedata_df.to_json(orient='records')
LineList = json.loads(Lines_json_str)

##Read Bus Data
BusList = []
excel_busdata_df = pandas.read_excel(DataFile, sheet_name=BusData_SheetName)
Buses_json_str = excel_busdata_df.to_json(orient='records')
BusList = json.loads(Buses_json_str)

# ********************************************************************



# *************************** Calculations ***************************************************
# ********************************************************************************************

##Create YBus Matrix
YBus_for_Studycase=YBus(LineList)
Y_Pol = YBus_for_Studycase.PolarForm()
Y_Rec= YBus_for_Studycase.CartesianForm()
#print(Y_Rec)
YBus_for_Studycase.write2excel('YBus.xlsx')

for i in range(max_iter):
    ##Calculate Power Mismatch
    del_PQ=del_Power.calculate_for(BusList,Y_Pol)
    #print('PQ',del_PQ)
    max_power_mismatch = max(np.abs(del_PorQ['del']) for del_PorQ in del_PQ)
    print('mismatch',max_power_mismatch)
    if max_power_mismatch<tollerance:
        break

    ##Calculate Jacobian Matrix
    
    JacobMatrix = Jacobian.calculate_for(BusList,Y_Rec,Y_Pol)
    print(JacobMatrix)
    #print(JacobMatrix)

    ##Update BusList with new Voltages
    Solved_BusVolts,BusList=BusVoltage.calculate_for(BusList,del_PQ,JacobMatrix)
    print('Number of Iteration is:',i)
    
#print('Number of Iteration is:',i)
LoadFlowList,LineLoss,Slack_Bus_Power=LoadFlow.calculate(Solved_BusVolts,LineList,Sbase)

# ********************************************************************************************








# *********************** Creating OutPut File ************************
# *********************************************************************

print(Solved_BusVolts)




writer = pandas.ExcelWriter('Load Flow Result.xlsx', engine= 'openpyxl')
workbook=writer.book
df1=pandas.DataFrame([{'Title':'No. of iteration required:  '+str(i)}])
df2=pandas.DataFrame([{'Title':' *******FINAL BUS VOLTAGES (in p.u.) ARE*******'}])
df_headerVolt=pandas.DataFrame([{'C1':'Bus No','C2':'Bus Code','C3':'Volt Mag (p.u.)','C4':'Volt Angle (rad)'}])
df3=pandas.DataFrame(Solved_BusVolts)
df4=pandas.DataFrame([{'Title':'   ************* LINE FLOWS *************   '}])
df_headerLineFlow=pandas.DataFrame([{'C1':'From Bus','C2':'To Bus','C3':'Active Power (MW)','C4':'Reactive Power (Mvar)'}])
df5=pandas.DataFrame(LoadFlowList)
df6=pandas.DataFrame([{'Title':'LINE Loss:'}])
df_headerLineLoss=pandas.DataFrame([{'C1':'MW','C2':'Mvar'}])
df7=pandas.DataFrame([{'MW':LineLoss.real,'Mvar':LineLoss.imag}])
df8=pandas.DataFrame([{'Title':'SLACK BUS POWER:'}])
df_headerSlackBus=pandas.DataFrame([{'C1':'MW','C2':'Mvar'}])
df9=pandas.DataFrame([{'MW':Slack_Bus_Power.real,'MVAR':Slack_Bus_Power.imag}])
df_signature=pandas.DataFrame([{'Title':'This Load Flow Study report is being prepared using python by:  DEBAJYOI GHOSH'}])
df_gap=pandas.DataFrame([{'Title':' '},{'Title':' '}])
DataFrames=[df1,df_gap,df2,df_headerVolt,df3,df_gap,df4,df_headerLineFlow,df5,df_gap,df6,\
            df_headerLineLoss,df7,df_gap,df8,df_headerSlackBus,df9,df_gap,df_gap,df_gap,df_signature]
lenght_of_data=0
header_rows=[]
insert_count=0
for df in DataFrames:
    insert_count+=1
    if insert_count in [1,3,7,11,15,21]:
        header_rows.append(lenght_of_data)
    df.to_excel(writer,sheet_name='Results',index=False, header=False,\
                startrow=lenght_of_data,startcol=1,float_format='%.4f')
    lenght_of_data+=df.shape[0]


workbook.save('Load Flow Result.xlsx')

workbook=openpyxl.load_workbook('Load Flow Result.xlsx')
worksheet=workbook['Results']
for row in header_rows:
    worksheet.merge_cells(start_row=row+1, start_column=2, end_row=row+1, end_column=8)

workbook.save('Load Flow Result.xlsx')

# ********************************************************************************************


