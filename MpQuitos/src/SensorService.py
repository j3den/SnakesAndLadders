import drivers.display.DisplayServiceSingleton as disp
import config.ConfigurationManager as cfm
import MpQuitos.drivers.sensors.DHT as dht
import json

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

    def collectSensorData(self):
        print("Collecting Data...")
        data_dict = []
        for sensor in _sensorSettings["sensors"]:
            s_type = sensor["type"]
            if s_type is "DHT11" or "DHT22":
                res = dht.DHTSensors().getValues(sensor)
                data_dict[s[name]] = res



