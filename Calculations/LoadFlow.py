import numpy as np
def calculate(BusList, LineList,Sbase):
    LineFlowList=[]
    LineLoss=0+0j
    Slack_Bus_Power=0+0j
    for line in LineList:
        i = line['From Bus']
        j = line['To Bus']
       
        if line['Tap Ratio']!=0 and line['Tap Ratio']<1:
            a=1/line['Tap Ratio']
            Yi0=a*a*line['B']+a*(a-1)/(line['R']+line['X']*1j)
            Yj0=line['B']+(1-a)/(line['R']+line['X']*1j)
        elif line['Tap Ratio']!=0 and line['Tap Ratio']>1:
            a=line['Tap Ratio']
            Yi0=line['B']+(1-a)/(line['R']+line['X']*1j)
            Yj0=a*a*line['B']+a*(a-1)/(line['R']+line['X']*1j)
        else: 
            a=1
            Yi0=Yj0=line['B']            
        Yij = 1*a/(line['R']+line['X']*1j)
        for Bus in BusList:
            if Bus['Bus No']==i:
                if Bus['Bus Code']==1: Is_I_Slack=1                   
                else: Is_I_Slack=0
                Vi=Bus['V']*np.exp(1j*Bus['delta'])
            elif Bus['Bus No']==j:
                if Bus['Bus Code']==1: Is_J_Slack=1                   
                else: Is_J_Slack=0
                Vj=Bus['V']*np.exp(1j*Bus['delta'])
        Sij=Vi*np.conjugate((Vi-Vj)*Yij+Vi*Yi0)
        LineFlow={'From Bus':i,'To Bus':j,'Active Power':Sij.real,'Reactive Power':Sij.imag}
        LineFlowList.append(LineFlow)
        Sji=Vj*np.conjugate((Vj-Vi)*Yij+Vj*Yj0)
        LineFlow={'From Bus':j,'To Bus':i,'Active Power':Sji.real,'Reactive Power':Sji.imag}
        LineFlowList.append(LineFlow)
        LineLoss+=(Sij+Sji)*Sbase
        if Is_I_Slack==1:Slack_Bus_Power+=Sji*Sbase            
        elif Is_J_Slack==1: Slack_Bus_Power+=Sji*Sbase

            
    return LineFlowList,LineLoss,Slack_Bus_Power