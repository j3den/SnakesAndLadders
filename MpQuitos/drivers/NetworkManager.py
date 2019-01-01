import _thread
import time

import drivers.display.DisplayServiceSingleton as disp
import network

import config.ConfigurationManager as cm


class WifiManager:
    _instance = None
    _print_text = disp.DisplaySingleService().print_text
    _clear_text = disp.DisplaySingleService().clear
    _statusCheckRunning = False
    _isConnected = False
    _isConnecting = False
    _SSID = ""
    _password = ""
    _threadCounter = 0
    _connectAttemptNum = 0

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(WifiManager, self).__new__(self)

            self.wifiSettings = cm.ConfigurationManager().getWifiConfig()
            self._SSID = self.wifiSettings["ssid"]
            self._password = self.wifiSettings["password"]
            self.wlan_intf = network.WLAN(network.STA_IF)
            self.wlan_intf.active(True)
            self._isConnected = False
            self._isConnecting = False


            print("init NetworkManager " + str(self._instance))
        return self._instance


    def scanForKnownNetworks(self):
        # Enable AP Wifi and scan for a known network
        wifiInterface = network.WLAN(network.STA_IF)
        wifiInterface.active(True)

        networks = wifiInterface.scan()

        for nw in networks:
            print (self.wifiSettings["ssid"])
            print("Found " + str(nw[0]))
            if nw[0].decode("utf-8") == self.wifiSettings["ssid"]:
                print(" I KNOW THIS ONE!")
                return True
        return False

    def enterAPMode(self):

        if not known_network_found:
            self._clear_text()
            self._print_text("No APs Found...",0)
            self._print_text("Entering APMode", 2)
            self._print_text("Use Mobile App.",4)
            self._print_text("to Set Up.", 5)
            wifiInterface = network.WLAN(network.AP_IF)
            wifiInterface.active(True)
            wifiInterface.config(essid="MOSQUITOX", authmode=3, password='1234567819')
            while wifiInterface.active() is not True:
                print("..." + str(wifiInterface.active()))
                time.sleep(1)

    def statusCheck(self):
        print("Wifi Status Check Started")

        while True:
            if self.wlan_intf.isconnected():
                self._isConnected = True
                self._isConnecting = False
                ip_addr = self.wlan_intf.ifconfig()[0]
                while len(ip_addr) < 15:
                    ip_addr = " " + ip_addr + " "
                self.displayConnected(ip_addr)
                time.sleep(3)

            else:
                self.displayLostConnection()
                self._isConnected = False
                self.connectToWlan()
                time.sleep(5)

    # Connect To WLAN

    def connectToWlan(self):

        def connect():




            self._isConnecting = True
            self._print_text(" !* Wifi *! ", 0)
            self._print_text("Connect Wifi", 1)
            self._print_text("Starting Up..", 2)

            try:
                self.wlan_intf.connect(self._SSID, self._password)
                x = 1
                while not self.wlan_intf.isconnected():
                    elipses = ""
                    for i in range(0, x % 4):
                        elipses = elipses + "."
                        self._print_text("Connecting" + elipses, 1)
                        self._print_text("To " + self._SSID, 2)
                    x = x + 1
                    time.sleep(0.5)
                self.isConnected = True
                self._isConnected = True
                self._isConnecting = False
                print("CONNECTED")
                self._clear_text()
                self._print_text(" !*Connected *!", 0)
                self._print_text("To: ", 1)
                self._print_text(self.wlan_intf.ifconfig()[2], 2)
                self._print_text(" ", 3)
                self._print_text("As IP:", 4)
                self._print_text(self.wlan_intf.ifconfig()[0], 5)
            except Exception as e:
                print("Connect Exception:" + str(e) + " : Attempt "+str(self._connectAttemptNum))
                self._connectAttemptNum = self._connectAttemptNum + 1
                #Redfine may help :S?
                self.wlan_intf = network.WLAN(network.STA_IF)
                time.sleep(5.0)
            time.sleep(2.0)
            self._clear_text()
            if not self._statusCheckRunning:
                self._statusCheckRunning = True
                _thread.start_new_thread(self.statusCheck, ())

        if not self._isConnected and not self._isConnecting:
            print("New Connect Thread: "+str(self._threadCounter))
            self._threadCounter = self._threadCounter + 1
            _thread.start_new_thread(connect, ())

    def displayLostConnection(self):
        self._clear_text()
        self._print_text("!!!!!!!!!!!!!!!!", 0)
        self._print_text("!    ERROR!    !", 1)
        self._print_text("!              !", 2)
        self._print_text("!     Lost     !", 3)
        self._print_text("!  Connection  !", 4)
        self._print_text("!!!!!!!!!!!!!!!!", 5)

    def displayConnected(self, ip_addr):

        self._print_text("!!!CONNECTED!!!", 0)
        self._print_text(ip_addr, 1)
        #####MESSAGE##########
        #####MESSAGE##########
        #####MESSAGE##########
        #####MESSAGE##########
