import gc
import config.ConfigurationManager as cm
import network
import time as time

print("Now Booting!")
print("Instantiating ConfigurationManager...")
configManager = cm.ConfigurationManager()

for e in configManager.getConfig():
    print(str(e))

print("Enabling and Setting GC threshold.\n")
gc.enable()
gc.collect()
# gc.set_threshold((gc.mem_alloc() + gc.mem_free())/5)

# Enable AP Wifi and scan:

wifiInterface = network.WLAN(network.AP_IF)
wifiInterface.active(True)
wifiInterface.config(essid="MOSQUITOX")
wifiInterface.config(authmode=3, password='1234567819')
time.sleep(2)

while wifiInterface.active is False:
    print("Active = "+str(wifiInterface.active()))
    time.sleep(1)
while True:
    networks = wifiInterface.scan()
    for nw in networks:
        print("Found " + nw.ssid)
    time.sleep(3)
