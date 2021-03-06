# SnakeAndLadders

# Introduction
Provides a config based MQTT IoT framework for ESP32 based boards using MicroPython.

# Config

Example:
PLACE IN /config/config.json
```json
{
  "unitSettings": {
    "Name": "MozzyY"
  },
  "wifiSettings": {
    "ssid": "PLUSNET-AAAA",
    "password": "s243dsds!2a"
  },
  "webServer": {
    "port": 80
  },
  "Display": {
    "ssd1306": true,
    "scl_pin": 15,
    "sda_pin": 4,
    "oled_reset_pin": 16,
    "width": 128,
    "height": 64
  },
  "MQTTSettings": {
    "server": "11.222.33.11",
    "username": "admin",
    "password": "MyActiveMQPassword",
    "authb64": "YWRtaW46RG9ua2V5U2FkZGxlMjE=",
    "defaultTopic": "Mosquito",
    "cacheFailedMessages":true,
    "port": 0
  },
  "RTCSettings":{
    "enabled":true,
    "initialValue":[2018,12,23,12,0,0,0,0],
    "enableUpdate":true,
    "updateServerURL":"http://worldclockapi.com/api/json/utc/now",
    "UTC_or_GMT":"UTC"
  }

}


```

# What is included (* in production)

1. A Mosquito (https://mosquitto.org/) publising service.
2. A NetworkManager to connect to Wifi.
3. An RTC Service to keep system time.
4. A DisplayService to use basic LCD screens (SSD1306) to easily display text.
