import numpy as np


def BPSK(bit_mass):
	di = []
	for i in range(len(bit_mass)):
		bi = bit_mass[i]
		real = (1 - 2 * bi) / np.sqrt(2)
		imag = (1 - 2 * bi) / np.sqrt(2)
		di.append(complex(real, imag)) 
	return np.asarray(di)


def QPSK(bit_mass):
	if (len(bit_mass) % 2 != 0):
		print("QPSK:\nError, check bit_mass length", len(bit_mass))
		raise "error"
	else:
		di = [] # массив комплексных чисел
		for i in range(0, len(bit_mass), 2):
			b2i = bit_mass[i]
			b2i1 = bit_mass[i+1]
			real = (1 - 2 * b2i) / np.sqrt(2)
			imag = (1 - 2 * b2i1) / np.sqrt(2)
			di.append(complex(real, imag))
		return np.asarray(di)

def QAM16(bit_mass):
	if (len(bit_mass) % 4 != 0):
		print("QAM16:\nError, check bit_mass length")
		raise "error"
	else:
		di = []
		for i in range(0, len(bit_mass), 4):
			b4i = bit_mass[i]
			b4i1 = bit_mass[i+1]
			b4i2 = bit_mass[i+2]
			b4i3 = bit_mass[i+3]
			real = (1 - 2 * b4i) * (2 - (1 - 2 * b4i2)) / np.sqrt(10)
			imag = (1 - 2 * b4i1) * (2 - (1 - 2 * b4i3)) / np.sqrt(10)
			di.append(complex(real, imag))
		return np.asarray(di)
	
def QAM64(bit_mass):
	if (len(bit_mass) % 6 != 0):
		print("QAM64:\nError, check bit_mass length")
		raise "error"
	else:
		di = []
		for i in range(0, len(bit_mass),6):
			b6i = bit_mass[i]
			b6i1 = bit_mass[i+1]
			b6i2 = bit_mass[i+2]
			b6i3 = bit_mass[i+3]
			b6i4 = bit_mass[i+4]
			b6i5 = bit_mass[i+5]
			real = (1 - 2 * b6i) * (4 - (1 - 2 * b6i2) * (2 - (1 - 2 * b6i4))) / np.sqrt(42)
			imag = (1 - 2 * b6i1) * (4 - (1 - 2 * b6i3) * (2 - (1 - 2 * b6i5))) / np.sqrt(42)
			di.append(complex(real, imag))
		return np.asarray(di)

def QAM256(bit_mass):
	if (len(bit_mass) % 8 != 0):
		print("QAM256:\nError, check bit_mass length")
		raise "error"
	else:
		di = []
		for i in range(0, len(bit_mass), 8):
			b8i = bit_mass[i]
			b8i1 = bit_mass[i+1]
			b8i2 = bit_mass[i+2]
			b8i3 = bit_mass[i+3]
			b8i4 = bit_mass[i+4]
			b8i5 = bit_mass[i+5]
			b8i6 = bit_mass[i+6]
			b8i7 = bit_mass[i+7]
			real = (1 - 2 * b8i) * (8 - (1 - 2 * b8i2) * (4 - (1 - 2 * b8i4) * (2 - (1 - 2 * b8i6)))) / np.sqrt(170)
			imag = (1 - 2 * b8i1) * (8 - (1 - 2 * b8i3) * (4 - (1 - 2 * b8i5) * (2 - (1 - 2 * b8i7)))) / np.sqrt(170)
			di.append(complex(real, imag))
		return np.asarray(di)
	
