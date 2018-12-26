import _thread
import time

import drivers.MQTTManager as mqm
import drivers.NetworkManager as nm
import drivers.RTCManager as rtcman
import src.MQService as mqs
import config.ConfigurationManager as cfm
import drivers.display.DisplayServiceSingleton as disp
import _thread

nameOfUnit = cfm.ConfigurationManager().getUnitConfig()["Name"]
RTCManager = rtcman.RTCManager()  # Instantiate RTC Manager
wifiManager = nm.WifiManager()  # Instantiate WifiManager
mQTTManager = mqm.MQTTManager()  # Instantiate MQTT Manager
wifiManager.connectToWlan()  # Connect To WLAN
mQTTManager.connect()  # Connect to MQ broker (ActiveMQ in my case).
webMQService = mqs.MQService()

_print_text = disp.DisplaySingleService().print_text
_clear_text = disp.DisplaySingleService().clear


def messageTests():
    x = 0

    while True:
        webMQService.addToQueue(nameOfUnit, "Hello!")
        mQTTManager.sendMessage("Hello! {}".format(str(x)))
        x = x + 1
        time.sleep(1)


try:
    _thread.start_new_thread(messageTests, ())
except Exception as e:
    print(e)
    _clear_text()
    chunked_message = ([str(e)[idx:idx + 16] for idx, val in enumerate(str(e)) if idx % 16 == 0])
    x = 0
    for i in chunked_message:
        if x < 6:
            _print_text(chunked_message[x], 0 + x)
        x = x + 1
