import numpy as np
import matplotlib.pyplot as plt
import MatchData as MD


"""
Changes data to standard form,
takes input as a vector
"""
def standardize_var(data):
    mean = np.mean(data, dtype=np.float64)
    std = np.std(data, dtype=np.float64)
    stan = (data - mean)/std
    return stan
"""
Tests two collections for
correlation also supplies a scatter plot
"""
def cor_test_plot(data1,data2):
    data = np.hstack((data1,data2)).transpose()
    cor = np.corrcoef(data)
    print(cor)
    t = np.arange(min(data2),max(data2),.2)
    plt.scatter(data2,data1)
    plt.plot(t + np.mean(data1),cor[1,0]*t + np.mean(data2),'r-')
    plt.show()

def main():
    reg_key = '2017mawor'
    opr = MD.getStat(reg_key,'teleopRotorPoints')
    ccwms = MD.getStat(reg_key,'autoPoints')
    cor_test_plot(opr,ccwms)

# To call main function
if '__main__' == __name__: main()
