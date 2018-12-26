import drivers.display.ssd1306 as ssd1306
import machine
import json


class DisplaySingleService():
    _instance = None
    lines = [""]*6
    displayEnabled = False

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(DisplaySingleService, self).__new__(self)
            print("init DisplayService " + str(self))
            config = open("config/config.json", "r")
            configDict = json.loads(config.read())
            displayDict = configDict["Display"]
            if displayDict.get("ssd1306") is True:
                self.displayEnabled = True
                print("SSD1306 Display init: scl = " + str(displayDict.get("scl_pin"))
                      + " sda = " + str(displayDict.get("sda_pin"))
                      + " oled_rst = " + str(displayDict.get("oled_rst_pin"))
                      + " width = " + str(displayDict.get("width"))
                      + " height = " + str(displayDict.get("height"))
                      )
                scl_pin = displayDict.get("scl_pin")
                sda_pin = displayDict.get("sda_pin")
                rst_pin = displayDict.get("oled_reset_pin")
                width = displayDict.get("width")
                height = displayDict.get("height")
                pin16 = machine.Pin(rst_pin, machine.Pin.OUT)
                pin16.value(1)
                i2c = machine.I2C(scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin))
                print("Initialises OLED from ssd1306.py lib dep")
                self.oled = ssd1306.SSD1306_I2C(width, height, i2c)
                print("Initialised " + str(self.oled))
        return self._instance

    def print_text(self,text,line):
        if self.displayEnabled:
            self.lines[line]=text
            x=0
            self.oled.fill(0)
            for i in range (0,len(self.lines)):
               self.oled.text(self.lines[i],0,x)
               x=x+10
            self.oled.show()

    def clear(self):
        if self.displayEnabled:
            self.lines = [""]*6

