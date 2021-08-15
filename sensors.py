#!/usr/bin/python
 
import spidev
import numpy as np

spi = spidev.SpiDev()


class Transducer:

    def __init__(self, device=0):
        spi.open(0, device)
        spi.max_speed_hz=1000000

 
    def read_channel(self, channel):
        val = spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((val[1] & 3) << 8) + val[2]
        return data

    def get_distance(self, channel, do_print=False):
        v = self.read_channel(channel) / 1023.0 * 3.3
        dist = 100.6336 * v**4 - 488.2443 * v**3 + 886.4260 * v**2 - 727.2917 * v + 244.9170
        if do_print:
            print(f'Distance to obstacle: {dist} cm.\n')
        return dist

    def get_all_distances(self):
        distances = list()
        for channel in range(7 + 1):
            distances.append(self.get_distance(channel))
        return distances

    # FIXME: function only reads and computes mean     
    def pseudo_calibrate(self, repeat=10, margin=0.05):
        values = list()
        for i in range(repeat): 
            v = (self.read_channel(0)/1023.0)*3.3
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
  



    