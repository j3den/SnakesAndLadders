import time
import drivers.display.DisplayServiceSingleton as disp
import json
import umqtt.simple as mq
import _thread
import config.ConfigurationManager as cm


class MQTTManager:
    _instance = None
    _print_text = disp.DisplaySingleService().print_text
    _clear_text = disp.DisplaySingleService().clear
    _statusCheckRunning = False
    _isConnected = False
    _isConnecting = False
    _messageCount = 0
    _brokerReconAttemptCount = 0

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(MQTTManager, self).__new__(self)

            self.mqttSettings = cm.ConfigurationManager().getMQTTConfig()
            self.unitSettings = cm.ConfigurationManager().getUnitConfig()

            self._server = self.mqttSettings["server"]
            self._username = self.mqttSettings["username"]
            self._password = self.mqttSettings["password"]
            self._default_topic = self.mqttSettings["defaultTopic"]
            self._clientId = self.unitSettings["Name"]
            self._port = self.mqttSettings["port"]

            self._mq_connection = mq.MQTTClient(client_id=self._clientId, server=self._server, port=self._port,
                                                user=self._username,
                                                password=self._password)

            print("Init MQTTManager " + str(self._instance))
        return self._instance

    def connect(self):
        self._isConnecting = True
        x = 0

        while not self._isConnected:

            try:
                self._mq_connection.connect()
                self._isConnected = True
                self._isConnecting = False
                self._clear_text()

            except Exception as e:
                self._isConnected = False
                self._mq_connection.sock.close()
                self._print_text(str(e), 2)
                self._print_text("MQTT Conn...",3)
                self._print_text("Attempt:"+str(self._brokerReconAttemptCount),4)
                self._brokerReconAttemptCount = self._brokerReconAttemptCount + 1
                time.sleep(2)

    def sendMessage(self, message):
        # Message is sent...if fail (exception) then it is added to re-try file.
        self._messageCount = self._messageCount + 1
        if self._isConnecting:
            self._clear_text()
            self._print_text("BrokerRecconect",2)
            self._print_text("Added to Retry!",3)
            self._print_text("Recon Attempt->",4)
            self._print_text(str(self._brokerReconAttemptCount), 5)

            # TODO implement an internal file Queueing service
        else:
            try:

                self._mq_connection.publish(retain=True, topic=self._default_topic, msg=self.formMessageObject(message))
                self._showMessageScreen(message)

            except Exception as ose:
                self._isConnected = False
                #TODO ADD TO Q
                if not self._isConnected and not self._isConnecting:
                    _thread.start_new_thread(self.connect, ())
                print(str(ose))

                self._print_text(str(ose), 3)
                print("OSError")

    def _showMessageScreen(self,message):
        chunked_message = ([message[idx:idx + 16] for idx, val in enumerate(message) if idx % 16 == 0])
        x = 0
        for i in chunked_message:
            if x < 4:
                self._print_text(chunked_message[x], 3 + x)
            x = x + 1

    def formMessageObject(self,message):
        #Create a message object...
        dictOb = {"UnitName":self._clientId,"Message":message}
        return json.dumps(dictOb)

