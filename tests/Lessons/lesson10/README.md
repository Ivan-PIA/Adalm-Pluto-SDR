# Lesson 10



1. Определяли корреляцию для кода Баркера

- Длина 5

```py
a = np.array([1, 1, 1, -1, 1])
b = np.correlate(a,a,'full')
```
<img src = "photo/Figure_2.png">


- Длина 11

```py
a = np.array([1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1])
b = np.correlate(a,a,'full')
```
<img src = "photo/Figure_1.png">



2. Сформированный модулированный сигнал


<img src = "photo/tx1.png">


3. Принятый сигнал ASK

<img src = "photo/csv.png">


- Принятые данные записали в файл для дальнейшей обработки


```py
np.savetxt (" my_data.csv", rx_data, delimiter=" , ")
```