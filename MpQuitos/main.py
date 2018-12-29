import _thread
import time

import network

import config.ConfigurationManager as cfm
import drivers.MQTTManager as mqm
import drivers.NetworkManager as nm
import drivers.display.DisplayServiceSingleton as disp
import src.MQService as mqs
import machine

configMan = cfm.ConfigurationManager()
nameOfUnit = cfm.ConfigurationManager().getUnitConfig()["Name"]
wifiManager = nm.WifiManager()  # Instantiate WifiManager
mQTTManager = mqm.MQTTManager()  # Instantiate MQTT Manager
wifiManager.connectToWlan()  # Connect To WLAN
mQTTManager.connect()  # Connect to MQ broker (ActiveMQ in my case).
webMQService = mqs.MQService()

_print_text = disp.DisplaySingleService().print_text
_clear_text = disp.DisplaySingleService().clear

# Enable AP Wifi and scan:
wifiInterface = network.WLAN(network.STA_IF)
wifiInterface.active(True)

networks = wifiInterface.scan()
known_network_found = False
for nw in networks:
    print (cfm.ConfigurationManager().getWifiConfig()["ssid"])
    print("Found " + str(nw[0]))
    if nw[0].decode("utf-8") == configMan.getWifiConfig()["ssid"]:
        print(" I KNOW THIS ONE!")
        known_network_found = True


# if not known_network_found:
#     _print_text("Entering APMode", 3)
#     wifiInterface = network.WLAN(network.AP_IF)
#     wifiInterface.active(True)
#     wifiInterface.config(essid="MOSQUITOX", authmode=3, password='1234567819')
#     while wifiInterface.active() is not True:
#         print("..." + str(wifiInterface.active()))
#         time.sleep(1)


def messageTests():
    x = 0
    while True:
        m = "Hello! {}".format(str(x))
        if webMQService.addToQueue(nameOfUnit, m):
            _print_text("WMQ ->", 4)
            _print_text(m, 5)
        x = x + 1
        machine.deepsleep(5*60*1000)


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
