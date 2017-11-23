# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 20:57:08 2017

@author: luxiaolei
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

def GenerateData(): #生成数据
    u=np.random.uniform(0,1,100)
    a0=8*np.exp(-(u-0.5)**2)
    a1=2*np.cos(2*np.pi*u)
    a2=5*(u-0.5)**2
    Beta=pd.DataFrame(np.array([a0,a1,a2]).T,columns=['a0','a1','a2'])
    
    x0=np.ones(100)
    x1=np.random.normal(0,1,100)
    x2=np.random.normal(0,1,100)
    X=pd.DataFrame(np.array([x0,x1,x2]).T,columns=['x0','x1','x2'])
    
    esp=np.random.normal(0,0.08,100)
    Y=a0*x0+a1*x1+a2*x2+esp
    return u,Beta,Y,X

class LLR(object): #局部线性回归估计 
    def __init__(self,t0,h,Y,t,X):
        self.index=t0
        self.h=h
        self.Y=Y
        self.t=t
        self.X=X
    
    def kernal(self,u): #核
        return 0.75*(1-u**2)*(u**2<1)
        
    def get_W(self): #权重
       return self.kernal(np.abs(self.t-self.t[self.index])/self.h)
   
    def beta(self): #估计t0处的beta值
        W=np.matrix(np.diag(self.get_W()))
        u=np.tile(self.t-self.t[self.index],self.X.shape[1]).reshape(self.X.shape,order='F')
        X=np.matrix(pd.concat([self.X,self.X*u],axis=1))
        return (X.T*W*X).I*X.T*W*np.matrix(self.Y).reshape(self.Y.shape[0],-1)
    
def AMS(m,Q,X,t,Y,h): #AMS交叉验证
    m=np.round(m*Y.shape[0])
    ams_q=0
    for q in np.arange(Q)+1:
        h_ams=h*(Y.shape[0]/(Y.shape-q*m))**0.2
#        训练
        index_train=np.arange(Y.shape[0]-q*m,dtype=int)
        Beta_est=pd.DataFrame()
        for t0 in index_train:
            Dat=LLR(t0,h=h_ams,Y=Y[index_train],t=t[index_train],X=X.iloc[index_train,:])   # 窗宽取了0.35
            try:
                result=pd.DataFrame(Dat.beta().T)
            except Exception as e:
                print(h,t0,Exception,":",e)
                result=pd.DataFrame([0,0,0,0,0,0]).T
            Beta_est=Beta_est.append(result)
        Beta_est=Beta_est.iloc[:,0:3]
#        测试
        index_test=np.arange(Y.shape[0]-q*m,Y.shape[0]-q*m+m,dtype=int)
        for t0 in index_test:
            k=np.abs(t[index_train]-t[t0])/h_ams
            kh=np.exp(-k)
#            print(pd.DataFrame((kh/np.sum(kh)).dot(Beta_est)).T)
            Beta_est=Beta_est.append(pd.DataFrame((kh/np.sum(kh)).dot(Beta_est.iloc[index_train,:])).T)
        Y_est=np.sum(Beta_est.values[index_test,:]*X.values[index_test,:],axis=1)
        ams_q+=np.mean((Y_est-Y[index_test])**2)
#        print(ams_q)
#        print(Beta_est.iloc[index_train,:])
    ams=ams_q/Q
    print(h,ams)
    return ams

#==============================================================================
# np.random.seed(666)
# u,Beta,Y,X=GenerateData()
# AMS(m=0.1,Q=4,X=X,t=u,Y=Y,h=0.01)
#==============================================================================
    
if __name__ == '__main__':
    np.random.seed(6)
    u,Beta,Y,X=GenerateData()
    h0=Y.shape[0]**-0.2
    h_cad=np.arange(0.01,1,0.01)
    ams=[AMS(m=0.1,Q=4,X=X,t=u,Y=Y,h=h) for h in h_cad]
    
#    a.iloc[a[1].argsort()[a[1].argsort().index<95],:]
    plt.scatter(h_cad,ams,s=5)
    plt.ylim(0,2)
    plt.show()
    
    h_opt=h_cad[ams==min(ams)]  #最优带宽
    print('the best h is :',str(h_opt[0]))
    
    Beta_est=pd.DataFrame()
    for t0,element in enumerate(Y):
        Dat=LLR(t0,h=h_opt,Y=Y,t=u,X=X)   # 窗宽取最优带宽
        try:
            result=pd.DataFrame(Dat.beta().T)
            Beta_est=Beta_est.append(result)
        except Exception as e:
            print(t0,e)
    
    Beta_est=Beta_est.iloc[:,0:3]
    Beta_est=Beta_est.reset_index(drop=True)
    Beta_est.columns=['a0','a1','a2']
#    print(Beta_est)
#    print(Beta_est-Beta)
    
    plt.style.use('ggplot')
#    plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签  
#    plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号      
    sortindex=np.copy(u.argsort())
    u=u[sortindex]
    Beta_est=Beta_est.iloc[sortindex,:]
    Beta=Beta.iloc[sortindex,:]
    
    plt.scatter(u,(Beta_est-Beta).iloc[:,0],s=5) #beta残差
    plt.show()
    
    plt.plot(u,Beta_est.iloc[:,0],'r--',label='true beta') #beta估计
    plt.legend(loc='upper right')
    plt.show()
    
    plt.plot(u,Beta.iloc[:,0],'b-.',label='estimated beta') #beta真值
    plt.legend(loc='upper right')
    plt.show()
    
    plt.plot(u,Beta_est.iloc[:,0],'r--',label='true beta') #beta估计
    plt.legend(loc='upper right')
    plt.plot(u,Beta.iloc[:,0],'b-.',label='estimated beta') #beta真值
    plt.legend(loc='upper right')
    plt.show()
    #plt.plot(u,Beta_est.iloc[:,0],'bs',u,Beta.iloc[:,0],'g^')
#    Y_est=np.sum(Beta_est.values*X.values,axis=1)
#    print(sum(sum((Beta.values-Beta_est.values)**2)/Beta.size)
#    print(np.mean((Y_est-Y)**2))
#    print(Beta_est.describe())


       
       
    


