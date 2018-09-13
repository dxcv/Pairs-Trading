import statsmodels.api as sm
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
t0=time.time()

#找出协整的股票对子
def cointergrate_function(dataframe):
    n = dataframe.shape[1]
    p_matrix = np.zeros([n, n])
    stock_ID = dataframe.columns
    pairs = []
    for i in range(n):
        for j in range(i+1,n):
            stock1 = dataframe[stock_ID[i]]
            stock2 = dataframe[stock_ID[j]]
            result = sm.tsa.stattools.coint(stock1, stock2)
            #print(result)
            pvalue = result[1]
            p_matrix[i, j] = pvalue
            p_matrix[j, i] = pvalue
            if pvalue < 0.05:
                pairs.append((stock_ID[i],stock_ID[j], pvalue))
    return p_matrix, pairs
df=pd.read_excel('BankData_Daily.xlsx',index_col='Time')
df=df.ix[0:607,:]
[p_matrix, pairs]=cointergrate_function(df)
print(pairs)
print(p_matrix)
#对对子进行ols回归
for i in range(len(pairs)):
    stock_1=df[pairs[i][0]]
    stock_2=df[pairs[i][1]]
    stock_1.plot()
    stock_2.plot()
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend([pairs[i][0],pairs[i][1]])
    #plt.show()
    S=sm.add_constant(stock_1)
    result=(sm.OLS(stock_2,S)).fit()
    print(result.summary())

df1=df.ix[:,1:3]
df2=df.ix[:,3:5]
#求每个对子的历史均值方差
m=[]
sigma=[]
list_1=df1.ix[:,1]-(1.2815*(df1.ix[:,0]))
sum_1=list_1.sum()
mean_1=sum_1/len(df1)
var_1=((list_1-mean_1)**2).sum()/(len(df1)-1)
sigma_1=var_1**0.5

list_2=df2.ix[:,1]-(0.7870*(df2.ix[:,0]))
sum_2=list_2.sum()
mean_2=sum_2/len(df2)
var_2=((list_2-mean_2)**2).sum()/(len(df2)-1)
sigma_2=var_2**0.5

m.append(mean_1)
m.append(mean_2)
sigma.append(sigma_1)
sigma.append(sigma_2)
print(m)
print(sigma)