import numpy as np



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


def CRC_RX(data):
    G = [1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,1]
    for i in range(0,len(data)-16):
        if(data[i] == 1):
            for j in range(len(G)):
                data[i+j] = data[i+j] ^ G[j]
    crc = data[len(data)-16:]

    return np.asarray(crc)    


data_bits =     [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1,1,1,0,1,0,0,0,0,1]

print(ADD_CRC(data_bits))
print(CRC_RX(ADD_CRC(data_bits)))