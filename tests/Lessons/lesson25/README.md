# Подсчет EVM. Реализация CRC. 


- EVM для QPSK

```py
def EVM_qpsk(qpsk):
    """
        `qpsk` - символы qpsk
        не демодулирует только считает ошибку
    """
    Co = np.array([1+1j, 1-1j, -1+1j, -1-1j]) 

    evm_sum = 0

    for i in range(len(qpsk)):
        t = 0
        temp = []
        for j in range(len(Co)):
            
            
            co2 = Co[j].real**2 + Co[j].imag**2

            evn2 =  (Co[j].real - qpsk[i].real)**2 + (Co[j].imag - qpsk[i].imag)**2

            evm = np.sqrt(evn2/co2)
            temp.append(evm)
        t = min(temp)
            
        evm_sum += t

    evm_db = np.abs(20 * np.log10(evm_sum/len(qpsk)))

    return evm_db
```

- Добавление CRC

```py
def ADD_CRC(data):
    """
        data - bits
        return : data + crc
    """

    G = [1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,1] # полином для вычисления crc

    data_crc = data + 16 * [0]
    for i in range(0,len(data_crc)-16):
        if(data_crc[i] == 1):
            for j in range(len(G)):
                data_crc[i+j] = data_crc[i+j] ^ G[j]
    crc = data_crc[len(data_crc)-16:]
    

    data = np.concatenate([data, crc])

    return data

```

