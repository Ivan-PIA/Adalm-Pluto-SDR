from context import QAM256, randomDataGenerator, plot

bit = randomDataGenerator(16000)
QAM256 = QAM256(bit)
plot(QAM256)