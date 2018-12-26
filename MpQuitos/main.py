import _thread
import time

import drivers.MQTTManager as mqm
import drivers.NetworkManager as nm
import drivers.RTCManager as rtcman
import src.MQService as mqs

RTCManager = rtcman.RTCManager()  # Instantiate RTC Manager
wifiManager = nm.WifiManager()  # Instantiate WifiManager
mQTTManager = mqm.MQTTManager()  # Instantiate MQTT Manager
wifiManager.connectToWlan()  # Connect To WLAN
mQTTManager.connect()  # Connect to MQ broker (ActiveMQ in my case).
mqs.MQService()


def messageTests():
    x = 0

    while True:
        mqs.MQService().addToQueue("httpservletreq", "Hello!{}".format(str(x)))
        mQTTManager.sendMessage("Hello! {}".format(str(x)))
        x = x + 1
        time.sleep(1)


_thread.start_new_thread(messageTests, ())
