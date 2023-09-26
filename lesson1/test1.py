import adi

#https://humble-ballcap-e09.notion.site/1b3f5d5dedb7422f8518bff7914d227c?pvs=4

sdr = adi.Pluto('ip:192.168.2.1') # адрес PlutoSDR
sdr.sample_rate = int(2.5e6) # колчество временных отсчето в 1 [сек]
rx_data = sdr.rx()
print("rx data length: ",len(rx_data))

for i in rx_data:
    print(i)