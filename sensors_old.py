#!/usr/bin/python
 
import spidev
import numpy as np
 
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
 
 
def readChannel(channel):
    val = spi.xfer2([1,(8+channel)<<4,0])
    data = ((val[1]&3) << 8) + val[2]
    return data

def calibrate(repeat=10, margin=0.05):
    values = list()
    for i in range(repeat): 
        v=(readChannel(0)/1023.0)*3.3
        values.append(v)
    
    values = np.array(values)
    avg = values.mean()
    print("Mean1 = ", avg)

    values2 = list()
    for elem in values: 
        if abs(elem - avg) < margin:
            values2.append(elem)

    values2 = np.array(values2)
    avg2 = values2.mean()
    print("Mean2 = ", avg2)    
  
if __name__ == "__main__":


    v=(readChannel(0)/1023.0)*3.3
    # # dist = 8.075 * v**4 - 68.44 * v**3 + 210.4 * v**2 - 285.2 * v + 161.3
    # dist =  27 / v 
    dist = 100.6336 * v**4 - 488.2443 * v**3 + 886.4260 * v**2 - 727.2917 * v + 244.9170
    print(f"Distance: {dist} cm\n") 