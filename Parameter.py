##As it have multiple returns from same calculation hence formed as class, not module
import numpy as np
import pandas
class YBus:
    def __init__(self, LineList) :
        self.LineList = LineList
        def pol2cart(r, theta):
            z = r * np.exp(1j * theta)
            x, y = z.real, z.imag
            return x, y


        def cart2pol(x, y):
            z = x + y * 1j
            num_pol = {"r": np.round(np.abs(z),5),"theta": np.round(np.angle(z),5)}
            return num_pol
        
        nb = max(max(line['From Bus'],line['To Bus']) for line in self.LineList) #defines the total number of buses. 
        self.Y = np.zeros((nb, nb), dtype=complex)

        ##Creating diagonal elements        
        for i in range(nb):
            print(nb)
            for line in self.LineList:
                if line['From Bus']==i+1 or line['To Bus']==i+1:
                    if line['Tap Ratio']!=0 and line['Tap Ratio']<1 and line['From Bus']==i+1:
                        a=1/line['Tap Ratio']
                    elif line['Tap Ratio']!=0 and line['Tap Ratio']>1 and line['To Bus']==i+1:
                        a=line['Tap Ratio']
                    else: a=1
                    print(i)
                    print('a',a)
                    print(self.Y[i,i])
                    print(line['From Bus'])
                    print(line['To Bus'])         
                    print(line['R'])    
                    print(line['X'])       
                    print(line['B'])                  
                    self.Y[i,i]+=1/(line['R']+line['X']*1j)*a*a+line['B']*1j
                    print(1/(line['R']+line['X']*1j))
                    print(self.Y[i,i])









        ##Creating off-diagonal elements
        for line in self.LineList:
            if line['Tap Ratio']!=0 and line['Tap Ratio']<1:
                a=1/line['Tap Ratio']
            elif line['Tap Ratio']!=0 and line['Tap Ratio']>1:
                a=line['Tap Ratio']
            else: a=1
            self.Y[line['From Bus']-1,line['To Bus']-1]=self.Y[line['To Bus']-1,line['From Bus']-1]=-1*a/(line['R']+line['X']*1j)


        #print(Y)

        ##Creating Y-Buss in polar form
        self.Y_Pol = []
        for i in range(nb):
            row = []
            for j in range(nb):
                row.append(cart2pol(self.Y[i,j].real,self.Y[i,j].imag))
            self.Y_Pol.append(row)

    def CartesianForm(self):
        return self.Y
    
    def PolarForm(self):
        return self.Y_Pol
    #print(Y_Pol[0][0]['theta'] )
    ##print(LineList)
    ##print(Y_Pol)
    def write2excel(self,File):
        #self.File=File
        df = pandas.DataFrame(self.Y).T
        df.to_excel(excel_writer = File)