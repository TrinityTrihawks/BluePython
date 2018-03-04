import numpy as np
import matplotlib.pyplot as plt
import MatchData as MD

def standardize_var(data):
    mean = np.mean(data, dtype=np.float64)
    std = np.std(data, dtype=np.float64)
    stan = (data - mean)/std
    return stan

def cor_test_plot(data1,data2):
    data = np.hstack((data1,data2)).transpose()
    print(data.shape)
    cor = np.corrcoef(data)
    print(cor)
    t = np.arange(min(data2),max(data2),.2)
    plt.scatter(data2,data1)
    plt.plot(t + np.mean(data1),cor[1,0]*t + np.mean(data2),'r-')
    plt.show()

def test():
    reg_key = "2017mnmi2"
    ccwms = standardize_var(MD.getCCWMS(reg_key))
    opr = standardize_var(MD.getOPRS(reg_key))
    data = np.hstack((ccwms,opr)).transpose()
    cor = np.corrcoef(data)
    print(cor)
    t = np.arange(min(opr),max(opr),.2)
    plt.scatter(ccwms,opr)
    plt.plot(t,cor[1,0]*t,'r-')
    plt.show()

def test2():
    arr = np.array([1,2,3,4])
    stan_arr = standardize_var(arr)
    print(stan_arr.transpose().dot(stan_arr))

def main():
    reg_key = '2017mawor'
    opr = MD.getStat(reg_key,'teleopRotorPoints')
    ccwms = MD.getStat(reg_key,'autoPoints')
    cor_test_plot(opr,ccwms)

# To call main function
if '__main__' == __name__: main()
