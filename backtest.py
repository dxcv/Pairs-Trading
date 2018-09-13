import statsmodels.api as sm
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt

def backtest(K,a,b,df,beta):
    signal = 0
    trade_times=0
    profit=0
    volume_long=[]
    volume_short=[]
    open_price_long=[]
    open_price_short=[]
    close_price_long=[]
    close_price_short=[]
    for i in range(len(df)):
        if abs(df.ix[i,1]-beta*df.ix[i,0])>a and signal==0:
            signal=1
            n=int(K*beta/(a-b))+1
            volume_long.append(n)
            open_price_long.append(df.ix[i,0])
            m=int(n/beta)+1
            volume_short.append(m)
            open_price_short.append(df.ix[i,1])
        if abs(df.ix[i,1]-beta*df.ix[i,0])<b and signal==1:
            trade_times+=1
            signal=0
            close_price_long.append(df.ix[i,0])
            close_price_short.append(df.ix[i,1])
    for i in range(trade_times):
        profit1=volume_long[i]*(close_price_long[i]-open_price_long[i])
        profit2=volume_short[i]*(open_price_short[i]-close_price_short[i])
        profit=profit+profit1+profit2
    return [trade_times,profit]

df=pd.read_excel('BankData_Daily.xlsx',index_col='Time')
df1=df.ix[607:-1,1:3]
df2=df.ix[607:-1,3:5]
beta=[1.2815,0.7870]
m=[0.3224491778418452, 0.42336713410214216]
sigma=[0.10632469454913575, 0.1546637614639448]
[trade_times1,profit1]=backtest(1000,m[0]+0.5*sigma[0],m[0],df1,beta[0])
print([trade_times1,profit1])
[trade_times2,profit2]=backtest(1000,m[1]+0.000001*sigma[1],m[1],df2,beta[1])
print([trade_times2,profit2])