# Прием OFDM. Частотная синхронизация


- реализовать Частотную синхронизацию 


```py
def Freq_Correction(rx_ofdm, Nfft, cp):

    for i in range(len(rx_ofdm)//(Nfft+cp)):
        
        e1 = rx_ofdm[(i * (Nfft + cp)) :( i * (Nfft + cp) + cp)]
        e2 = rx_ofdm[(i * (Nfft + cp) + Nfft):(i * (Nfft + cp) + (Nfft+cp))]
        sum = abs(np.sum(np.conjugate(e1) * e2)/(np.pi*2))
        ic(sum)

        n_new = 0 
        for n in range(i*(Nfft+cp) + cp,(i+1) * (Nfft+cp)):
            rx_ofdm[n] = rx_ofdm[n] * np.exp(-1j * 2 * np.pi * (sum/Nfft) * n_new)
            n_new += 1 
            #print(n)
        n_new = 0    
    return rx_ofdm

   
```

- Вторая Частотная синхронизация по двум соседним ofdm-символам.


```py
def Classen_Freq(rx_sig,  Nfft, pilot, index_pilot):
    eps_all = []
    eps = 0
    index_pilot = index_pilot[1:]
    
    
    for i in range(-20,20):

        y_e = rx_sig[index_pilot]
        for j in range(len(y_e)//2):
            eps += (pilot * np.conjugate(pilot) * y_e[j] * np.conjugate(y_e[j+6]))/ (np.pi * Nfft)
            #print(j)
        
        eps_all.append(abs(eps))
        ic(index_pilot + i)
        y_e = rx_sig[index_pilot]
        eps = 0

    max_eps = np.max(eps_all)
    ic(eps_all)
    for i in range(len(rx_sig)//(Nfft)):
        n_new = 0 
        for n in range(i*(Nfft),(i+1) * (Nfft)):
            rx_sig[n] = rx_sig[n] * np.exp(-1j * 2 * np.pi * max_eps/Nfft * n_new)
            n_new += 1 
            #print(n)
        n_new = 0 
    return rx_sig 
```

- что первая, что вторая не работает