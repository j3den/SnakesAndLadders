import dht
import machine
import time
import MpQuitos.config

class DHTSensors:

    def getValues(self):
        #Load config
        d = dht.DHT11(machine.Pin(pin))
        d.measure()
        time.sleep(0.1)
        vals = (d.temperature(),d.humidity())

        print (vals)
        return vals


