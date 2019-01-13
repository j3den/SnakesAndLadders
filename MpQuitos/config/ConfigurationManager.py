import json

class ConfigurationManager:
    _instance = None

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(ConfigurationManager, self).__new__(self)
            self._config = json.loads(open("config/config.json", "r").read())
            self._wifi_config = self._config["wifiSettings"]
            self._display_config = self._config["Display"]
            self._web_server_config = self._config["webServer"]
            self._MQTT_config = self._config["MQTTSettings"]
            self._rtc_config = self._config["RTCSettings"]
            self._unitConfig = self._config["unitSettings"]
            self._sensorConfig = self._config["SensorSettings"]
            print("Init ConfigurationManager " + str(self._instance))
        return self._instance

    def getConfig(self):
        return self._config

    def getWifiConfig(self):
        return self._wifi_config

    def getDisplayCondif(self):
        return self._display_config

    def getWebServerConfig(self):
        return self._web_server_config

    def getMQTTConfig(self):
        return self._MQTT_config

    def getRTCConfig(self):
        return self._rtc_config

    def getUnitConfig(self):
        return self._unitConfig

    def getSensorConfig(self):
        return self._sensorConfig


