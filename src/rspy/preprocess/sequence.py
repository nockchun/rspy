import numpy as np

def genSequence(data, windowSize, labelSize=1):
    seqData = data[:-(windowSize+labelSize-1)].reshape(-1, 1)
    seqLabel = data[windowSize:-(labelSize-1) if labelSize > 1 else None].reshape(-1, 1)
    for idx in range(1, windowSize):
        seqData = np.concatenate([seqData, data[idx:-(windowSize+labelSize-idx-1)].reshape(-1, 1)], axis=1)
    for idx in range(1, labelSize):
        lastIdx = labelSize-idx-1
        seqLabel = np.concatenate([seqLabel, data[windowSize+idx:-lastIdx if lastIdx > 0 else None].reshape(-1, 1)], axis=1)
    return seqData, seqLabel