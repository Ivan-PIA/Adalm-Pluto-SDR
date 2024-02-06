from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot
import matplotlib.pyplot as plt

bit = randomDataGenerator(24000)
QAM256 = QAM256(bit)
QAM64 = QAM64(bit)
QAM16 = QAM16(bit)
QPSK = QPSK(bit)

plot(QPSK)

plot(QAM16)

plot(QAM64)

plot(QAM256)