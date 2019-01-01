import dht
import machine

class DHT22Sensor:

    def getValues(self,pin):
        d = dht.DHT11(machine.Pin(pin))
        result = d.measure()
        print (result)
        return result
