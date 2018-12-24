import _thread
import time

import drivers.MQTTManager as mqm
import drivers.NetworkManager as nm
import drivers.RTCManager as rtcman

RTCManager = rtcman.RTCManager()  # Instantiate RTC Manager
wifiManager = nm.WifiManager()  # Instantiate WifiManager
mQTTManager = mqm.MQTTManager()  # Instantiate MQTT Manager
wifiManager.connectToWlan()  # Connect To WLAN
mQTTManager.connect()  # Connect to MQ broker (ActiveMQ in my case).


def messageTests():
    x = 0
    while True:
        mQTTManager.sendMessage("Hello!Hello!Hello!Hello!Hello!Hello!Hello! {}".format(str(x)))
        x = x + 1


_thread.start_new_thread(messageTests, ())
