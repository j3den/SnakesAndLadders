import drivers.NetworkManager as nm
import json
import src.display.DisplayServiceSingleton as disp
import time
import drivers.MQTTManager as mqm
import _thread
import gc
import drivers.RTCManager as rtcman

# Test reception e.g. with:
# mosquitto_sub -t foo_topic

config = json.loads(open("config/config.json").read())
displayService = disp.DisplaySingleService()

RTCManager = rtcman.RTCManager()
wifiManager = nm.WifiManager()
mQTTManager = mqm.MQTTManager()

wifiManager.connectToWlan()
printToScreen = displayService.print_text

mQTTManager.connect()


def messageTests():
    x = 0
    while True:
        mQTTManager.sendMessage("Hello! {}".format(str(x)))
        x = x + 1
        time.sleep(10)


_thread.start_new_thread(messageTests, ())
