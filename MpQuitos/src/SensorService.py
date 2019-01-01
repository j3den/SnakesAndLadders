import drivers.display.DisplayServiceSingleton as disp
import config.ConfigurationManager as cfm
import drivers.sensors.DHT22 as dht22


class SensorService:
    _instance = None
    _sensorSettings = cfm.ConfigurationManager().getSensorConfig()
    _print_text = disp.DisplaySingleService().print_text
    _clear_text = disp.DisplaySingleService().clear

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(SensorService, self).__new__(self)

            print("Init SensorService " + str(self._instance))

        return self._instance

    def getDHT22Values(self):
        a = dht22.DHT22Sensor().getValues(22)
        print (a)
