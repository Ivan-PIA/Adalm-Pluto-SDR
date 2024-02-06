from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot_QAM
import matplotlib.pyplot as plt

bit = randomDataGenerator(24000)
QAM256 = QAM256(bit)
QAM64 = QAM64(bit)
QAM16 = QAM16(bit)
QPSK = QPSK(bit)

plot_QAM(QPSK)

plot_QAM(QAM16)

plot_QAM(QAM64)

plot_QAM(QAM256)