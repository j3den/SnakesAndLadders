import json

import src.display.DisplayServiceSingleton as disp
import machine
import utime


class RTCManager:
    _instance = None
    _print_text = disp.DisplaySingleService().print_text
    _clear_text = disp.DisplaySingleService().clear
    _rtc = None

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(RTCManager, self).__new__(self)

            # Get Config...
            config = json.loads(open("config/config.json", "r").read())
            self.RTCSettings = config["RTCSettings"]

            if self.RTCSettings.get("enabled", False) is True:
                print("Enabling RTCManager")
                self._rtc = machine.RTC()
                # Set initial from config:
                configInitTime = self.RTCSettings.get("initialValue", None)
                if configInitTime is not None:
                    # YYYY,mm,dd,HH,mm,ss,us
                    print (str(configInitTime))
                    #timeTup = tuple()
                    #for t in configInitTime.split(","):
                       # timeTup.p
                    #self._rtc.datetime(tupleA)

            print("Init RTCManager " + str(self._instance))
        return self._instance