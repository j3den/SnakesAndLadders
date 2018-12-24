import time
import drivers.display.DisplayServiceSingleton as disp
import json
import umqtt.simple as mq
import _thread


class MQTTManager:
    _instance = None
    _print_text = disp.DisplaySingleService().print_text
    _clear_text = disp.DisplaySingleService().clear
    _statusCheckRunning = False
    _isConnected = False
    _isConnecting = False

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(MQTTManager, self).__new__(self)
            config = json.loads(open("config/config.json", "r").read())
            self.mqttSettings = config["MQTTSettings"]
            self._server = self.mqttSettings["server"]
            self._username = self.mqttSettings["username"]
            self._password = self.mqttSettings["password"]
            self._default_topic = self.mqttSettings["defaultTopic"]
            self._clientId = self.mqttSettings["clientId"]
            self._port = self.mqttSettings["port"]

            self._mq_connection = mq.MQTTClient(client_id=self._clientId, server=self._server, port=self._port,
                                                user=self._username,
                                                password=self._password)

            print("Init MQTTManager " + str(self._instance))
        return self._instance

    def connect(self):
        self._isConnecting = True
        while not self._isConnected:
            try:
                self._mq_connection.connect()
                self._isConnected = True
                self._isConnecting = False
            except Exception as e:
                self._isConnected = False
                self._mq_connection.sock.close()
                self._print_text(str(e), 2)
                time.sleep(2)

    def sendMessage(self, message):
        # Message is sent...if fail (exception) then it is added to re-try file.
        if self._isConnecting:
            print ("Currently attempting to Connect to Broker: Adding message to retry queue.\n")
            # TODO implement an internal file Queueing service
        else:
            try:
                c = bytearray(message)
                self._mq_connection.publish(retain=True, topic=self._default_topic, msg=c)

                chunked_message = ([message[idx:idx + 16] for idx, val in enumerate(message) if idx % 16 == 0])
                x = 0
                for i in chunked_message:
                    if x < 4:
                        self._print_text(chunked_message[x], 3 + x)
                    x = x + 1

            except Exception as ose:
                self._isConnected = False
                print ("Adding " + message + " to retry")
                if not self._isConnected and not self._isConnecting:
                    _thread.start_new_thread(self.connect, ())

                print(str(ose))
                self._print_text("FAILED TO SEND!", 1)
                self._print_text("ADDED TO RETRY!", 3)
                self._print_text(str(ose), 3)
                print("OSError")
