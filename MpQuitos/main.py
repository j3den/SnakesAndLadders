import _thread
import time
import machine
import config.ConfigurationManager as cfm
import drivers.NetworkManager as nm
import drivers.display.DisplayServiceSingleton as disp
import src.MQService as mqs
import src.SensorService as sensorService
import dht

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

    while True:
        led = machine.Pin(14, machine.Pin.OUT)
        d = dht.DHT11(machine.Pin(17))

        d.measure()
        temp = d.temperature()
        humidity = d.humidity()
        m = "{\"temperature\":\"" + str(temp) + "\",\"humidity\":\"" + str(humidity) + "\"}"
        if webMQService.addToQueue(nameOfUnit, m):
            led.value(1)
            _print_text("WMQ ->", 4)
            _print_text(m, 5)
            time.sleep(1)
            led.value(0)
            _clear_text()
            time.sleep(1)

        machine.deepsleep(15*60 * 1000)


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
    machine.deepsleep(15 * 60 * 1000)

