import numpy as np
import WebIntregration/MatchData as MD

def standardize_var(data):
    mean = np.mean(data)
    std = np.std(data)
    stan = (data - mean)/std
    return stan
