import drivers.WebRequestsService as wrs
import config.ConfigurationManager as cfm
import drivers.display.DisplayServiceSingleton as disp

import json


class MQService:
    _instance = None
    _mq_settings = None
    _auth = None
    _print_text = disp.DisplaySingleService().print_text
    _clear_text = disp.DisplaySingleService().clear

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(MQService, self).__new__(self)
            self.unitSettings = cfm.ConfigurationManager().getUnitConfig()
            self._webrequests_service = wrs.WebRequestsService()
            self._mq_settings = cfm.ConfigurationManager().getMQTTConfig()
            self._auth = self._mq_settings.get("authb64")
            self._clientId = self.unitSettings["Name"]
            print("Init MQService " + str(self._instance))
            self._authHeader = {"Authorization": "Basic " + self._auth,
                                "Content-Type": "application/x-www-form-urlencoded"}

            self._server = "http://" + self._mq_settings["server"] + ":8161/api/message/"

        return self._instance

    def addToQueue(self, queueName, message):
        try:
            url = self._server + queueName + "?type=queue"

            resp = self._webrequests_service.postRequest(destination=url,
                                                         content="body=" + self.formMessageObject(message),
                                                         headers=self._authHeader)

            if resp.status_code is not 200:
                print("Not got a 200...got : " + str(resp.status_code))
                self._print_text("WMQERR:" + str(resp.status_code), 2)
                return False  # Failed...

            return True  # Success...

        except Exception as e:
            self._print_text("WMQEXP:" + str(e), 2)
            print ("MQ Exception ->" + str(e))
            return False

    def formMessageObject(self, message):
        # Create a message object...
        dictOb = {"UnitName": self._clientId, "Message": message}
        return json.dumps(dictOb)
