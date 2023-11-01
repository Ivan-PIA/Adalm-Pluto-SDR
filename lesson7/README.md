# Lesson 7


### Lecture

<details>
1. Косинус

<img src="photo/cos.png"> 


2. Синус

<img src="photo/sin.png">

3. Символ КАМ модулированного сигнала 

<img src="photo/simbol_qam.png">

4. Шум

<img src="photo/noise.png">

5. Cимвол КАМ модулированного сигнала с шумом

<img src="photo/qam_with_noise.png">

6. Модуль спектра КАМ модулированного сигнала

<img src="photo/spectr_qam.png">

7. Модуль спектра символа после умножения на опорный косинус в приемнике

<img src="photo/modul_spectrum.png">

8. Импульсная характеристика цифрового ФНЧ

<img src="photo/fnc.png">

9. Фильтрация в фнч косинусной части принятого сигнала

<img src="photo/filter.png">

10. фильтрация в фнч синусной части принятого сигнала

<img src="photo/filter2.png">
</details>

### Practic

1. Передайте синусойду в рамках одного ADALM Pluto SDR. 

- Генерируемые вами значения должны быть комплексными, а значит, необходимо формировать две составляющие, реальную и мнимую. Например:

```py
i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
```

- Подаем на передатчик

```py 
samples = i + 1j * q 
```
<img src = "photo/photo_2023-11-01_10-00-36.jpg">

2. Спектр полученного сигнала

<img src = "photo/photo_2023-11-01_10-01-02.jpg">

3. Генерируем QPSK-модулированный сигнал, 16 сэмплов на символ

```py
num_symbols = 1000
x_int = np.random.randint(0, 4, num_symbols) # 0 to 3
x_degrees = x_int*360/4.0 + 135 # 45, 135, 225, 315 град.
x_radians = x_degrees*np.pi/180.0 # sin() и cos() в рад.
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) #генерируем комплексные числа
samples = np.repeat(x_symbols, 16) # 16 сэмплов на символ
samples *= 2**14 #Повысим значения для наших сэмплов
```

Приятые данные

<img src = "photo/photo_2023-11-01_10-01-45.jpg">

<img src = "photo/photo_2023-11-01_10-02-02.jpg">


