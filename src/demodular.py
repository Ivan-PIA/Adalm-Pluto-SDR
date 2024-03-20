import numpy as np


def DeQPSK(sample):

    bit = []
    for i in range(len(sample)):
        if sample.real[i] > 0 and sample.imag[i] > 0:
            bit.append(0)
            bit.append(0)

        if sample.real[i] < 0 and sample.imag[i] > 0:
            bit.append(1)
            bit.append(0)

        if sample.real[i] > 0 and sample.imag[i] < 0:
            bit.append(0)
            bit.append(1)

        if sample.real[i] < 0 and sample.imag[i] < 0:
            bit.append(1)
            bit.append(1)
        
    return np.asarray(bit)