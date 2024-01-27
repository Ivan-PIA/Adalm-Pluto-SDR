# Lesson 11


## AM модуляция

- Отправленные не преобразованные отчеты:

<img src = "photo/tx_IQ.png">

- Принятый сигнал после свертки:

<img src = "photo/convolve.png">


## QPSK модуляция

- Отправленные qpsk отчеты 

<img src = "photo/qpsk_tx.png">


- Принятый QPSK сигнал сразу:

<img src = "photo/qpsktx1.png">


- Принятый QPSK сигнал усреднение и уввеличение амплитуды:

```py
xrec = data_rx/np.mean(data_rx**2)
```

<img src = "photo/qpsk_mean.png">

