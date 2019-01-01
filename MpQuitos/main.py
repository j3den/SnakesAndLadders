import _thread
import time
import machine
import config.ConfigurationManager as cfm
import drivers.NetworkManager as nm
import drivers.display.DisplayServiceSingleton as disp
import src.MQService as mqs
import src.SensorService as sensorService

configMan = cfm.ConfigurationManager()
nameOfUnit = cfm.ConfigurationManager().getUnitConfig()["Name"]
wifiManager = nm.WifiManager()  # Instantiate WifiManager
webMQService = mqs.MQService()
sensorManager = sensorService.SensorService()
_print_text = disp.DisplaySingleService().print_text
_clear_text = disp.DisplaySingleService().clear

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=40000)
i2c.init(scl=machine.Pin(5), sda=machine.Pin(4), freq=40000)
print("SCANNIGN!!")
for f in i2c.scan():
    print(f)


def messageTests():
    stored_x = machine.RTC().memory()
    if len(stored_x)>0:
        x = int(str(stored_x))
        print(stored_x + " is type "+str(type(stored_x)))
    else:
        x = 0
    while True:
        m = "Hello! {}".format(str(x))
        if webMQService.addToQueue(nameOfUnit, m):
            _print_text("WMQ ->", 4)
            _print_text(m, 5)
        machine.RTC.memory(str(x+1).encode('utf-8'))
        machine.deepsleep(10 * 1000)


# Scan for known networks and connect if found:
if wifiManager.scanForKnownNetworks():
    wifiManager.connectToWlan()

    while not wifiManager._isConnected:
        print ("Connecting...")
        time.sleep(0.3)

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
else:
    wifiManager.enterAPMode()

_thread.start_new_thread(messageTests, ())
