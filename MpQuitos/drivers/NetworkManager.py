import network
import time
import _thread
import src.display.DisplayServiceSingleton as disp
import json


class WifiManager:
    _instance = None
    _print_text = disp.DisplaySingleService().print_text
    _clear_text = disp.DisplaySingleService().clear
    _statusCheckRunning = False
    _isConnected = False
    _SSID = ""
    _password = ""

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(WifiManager, self).__new__(self)
            config = json.loads(open("config/config.json", "r").read())
            self.wifiSettings = config["wifiSettings"]
            self._SSID = self.wifiSettings["ssid"]
            self._password = self.wifiSettings["password"]
            self.wlan_intf = network.WLAN(network.STA_IF)
            self.wlan_intf.active(True)
            self._isConnected = False

            print("init NetworkManager " + str(self._instance))
        return self._instance

    def statusCheck(self):
        print("Wifi Status Check Started")
        while True:
            # Pre-load print_text method

            if self.wlan_intf.isconnected:
                self._isConnected = True
                ip_addr = self.wlan_intf.ifconfig()[0]
                while len(ip_addr) < 15:
                    ip_addr = " " + ip_addr + " "

                self._clear_text()
                self._print_text("!!!!!!!!!!!!!!!!", 0)
                self._print_text("!   CONNECTED  !", 1)
                self._print_text("!              !", 2)
                self._print_text(ip_addr, 3)
                self._print_text("!              !", 4)
                self._print_text("!!!!!!!!!!!!!!!!", 5)
                time.sleep(15)


            else:
                self.isConnected = False
                self._clear_text()
                self._print_text("!!!!!!!!!!!!!!!!", 0)
                self._print_text("!    ERROR!    !", 1)
                self._print_text("!              !", 2)
                self._print_text("!     Lost     !", 3)
                self._print_text("!  Connection  !", 4)
                self._print_text("!!!!!!!!!!!!!!!!", 5)
                self.wlan_intf.connect()
                time.sleep(5)

    # Connect To WLAN
    # TODO...Could be done on separate thread...so other services can still run/not be blocked.
    def connectToWlan(self):
        self._print_text(" !* Wifi *! ", 0)
        self._print_text("Connect Wifi", 1)
        self._print_text("Starting Up..", 2)

        self.wlan_intf.connect(self._SSID, self._password)
        x = 1
        while not self.wlan_intf.isconnected():
            elipses = ""
            for i in range(0, x % 4):
                elipses = elipses + "."
                self._clear_text()
                self._print_text("Connecting" + elipses, 4)
                self._print_text("To " + self._SSID, 5)
            x = x + 1
            time.sleep(0.5)
        self.isConnected = True
        print("CONNECTED")
        self._clear_text()
        self._print_text(" !*Connected *!", 0)
        self._print_text("To: ", 1)
        self._print_text(self.wlan_intf.ifconfig()[2], 2)
        self._print_text(" ", 3)
        self._print_text("As IP:", 4)
        self._print_text(self.wlan_intf.ifconfig()[0], 5)

        time.sleep(2.0)

        if not self._statusCheckRunning:
            self._statusCheckRunning = True
            _thread.start_new_thread(self.statusCheck, ())

    def get_connected(self):
        time.sleep(0.5)
        return self.isConnected
