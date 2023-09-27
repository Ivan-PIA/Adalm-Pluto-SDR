# LESSON_3


1. При помощи приложения на **WifiAnalyzer** нашли канал наиболее мощной точки доступа из __скриншота__ ниже мы видим, что это точка доступа с **SSID OnePlus 9R**

![](https://github.com/Ivan-PIA/Adalm-Pluto-SDR/blob/main/lesson3/photo/photo_2023-09-27_22-36-51.jpg)

В **WifiAnalyzer** есть информация о ___канале___ и __несущей частоте__ в этом канале (обычно это центральная частота) у нас __2 канал__ и __частота 2417 МГц__

### 2. Разбирем код

- Библиотеки

```py
import time                     # для измененя частоты смены кадров 
import adi                      # для работы с Adalm-Pluto
import matplotlib.pyplot as plt # для отрисовки графика
import numpy as np              # для выделения реальной и мнимой части
```

- Подключаемся к SDR

```py
sdr = adi.Pluto("ip:192.168.2.1") # подключаемся к SDR
```

- Устанавливаем значение ***несущей частоты*** в соответствии с каналом

```py
sdr.rx_lo = 2417000000
```

- Сбор данных и отрисовка графиков

```py
for r in range(30):     #кол-во кадров с графиками
    rx = sdr.rx()       # принятые данные помещаем в rx
    plt.clf()           # на каждой итерации очищение старого графика
    plt.plot(rx.real)   # отрисовываем реальную часть
    plt.plot(rx.imag)   # отрисовываем мнимую часть
    plt.draw()          # пересовываем фигуру
    plt.xlabel('time')
    plt.ylabel('ampl')
    plt.pause(0.05)     # небольшая пауза перед отрисовкой, чтобы успеть обработать данные
    time.sleep(0.1)     # время смены кадра 
    
    # усреднение шума и сигнала p.s. требуется подтверждение преподавателя легально ли?
    for i in range(len(rx.imag)):  
       s+=rx.imag[i]               # сумма мнимых значений
    sred=s/len(rx.imag)            # считаем среднюю 
    if rx.imag[r]>sred:            # сравнимаем среднее значение со всеми мнимыми элементами  
        time.sleep(2)              # получаем задержку где колебания усреднены и не выше средней
    #print(sred)

plt.show()# #выводим график
```

## Результат :

![](https://github.com/Ivan-PIA/Adalm-Pluto-SDR/blob/main/lesson3/photo/photo_2023-09-27_22-33-06.jpg) 
![](https://github.com/Ivan-PIA/Adalm-Pluto-SDR/blob/main/lesson3/photo/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202023-09-27%2018-11-59.png)
![](https://github.com/Ivan-PIA/Adalm-Pluto-SDR/blob/main/lesson3/photo/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202023-09-27%2018-12-07.png) 
![](https://github.com/Ivan-PIA/Adalm-Pluto-SDR/blob/main/lesson3/photo/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202023-09-27%2018-12-26.png)
