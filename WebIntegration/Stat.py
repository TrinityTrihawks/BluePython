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
correlation and egression also supplies a scatter
"""
def cor_test_plot(data1,data2):
    data = np.hstack((data1,data2)).transpose()
    cor = np.corrcoef(data)

    #
    reg = np.polyfit(data1.flatten(),data2.flatten(),1)

    print("Correlation:" + str(cor[1,0]))
    print("Regression:" + str(reg[0]))

    t = np.arange(min(data1),max(data1),.2)
    plt.scatter(data1,data2)
    plt.plot(t,reg[0]*t + reg[1],'r-')
    plt.show()

def main():
    reg_key = '2018ndgf'
    opr = MD.getStat(reg_key,'totalPoints')
    ccwms = MD.getStat(reg_key,'autoPoints')
    cor_test_plot(opr,ccwms)

# To call main function
if '__main__' == __name__: main()
