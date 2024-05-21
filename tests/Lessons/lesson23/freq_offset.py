from scipy.io import loadmat, savemat
import matplotlib.pyplot as plt
import numpy as np
from context import *
from icecream import ic




def calculate_correlation(pss, matrix_name, m):
  """
  Calculates correlation between pss and matrix_name with filtering and delay.

  Args:
      pss: The reference signal.
      matrix_name: The signal to compare with pss.
      m: Decimation factor.

  Returns:
      A tuple containing the correlation and carrier frequency offset (CFO).
  """
  L = len(pss)

  # Flipped and complex conjugated reference signal
  corr_coef = np.flip(np.conj(pss))

  # Filter reference signal sections
  partA = np.convolve(corr_coef[:L // 2], matrix_name, mode='same')
  xDelayed = np.concatenate((np.zeros(L // 2), matrix_name[:-L // 2]))
  partB = np.convolve(corr_coef[L // 2:], xDelayed, mode='same')

  # Calculate correlation and phase difference
  correlation = np.abs(partA + partB)
  phaseDiff = partA * np.conj(partB)

  # Find maximum correlation and corresponding phase difference
  istart = np.argmax(correlation)
  phaseDiff_max = phaseDiff[istart]

  # Calculate CFO
  CFO = np.angle(phaseDiff_max) / (np.pi * 1 / m)
  t = np.arange(0,len(data))
  t = t / 1920000

 
  data_offset = matrix_name * np.exp(-1j * 2 * np.pi * np.conjugate(CFO) * t)

  return data_offset, correlation

# Example usage (assuming pss, matrix_name, and m are defined)

data = loadmat("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson23\\file_.mat_for_matlab\\rx_berore_2_sdr_ar.mat")

pss =  loadmat("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson23\\pss_time.mat")

h = list(pss.values())
pss = np.asarray(h[3])

h = list(data.values())
data = np.asarray(h[3])


pss = np.ravel(pss)
data = np.ravel(data)

print(len(pss))



data , correlation = calculate_correlation(pss, data, 15000)



plt.plot(correlation)


plt.show()