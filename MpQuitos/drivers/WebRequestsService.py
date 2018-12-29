import urequests


class WebRequestsService:
    _instance = None

    def __new__(self):
        print(self._instance)
        if not self._instance:
            self._instance = super(WebRequestsService, self).__new__(self)
            print("Init WebRequestsService " + str(self._instance))
        return self._instance

    def postRequest(self, destination, content, headers):
        payload = content.encode('utf-8')
        req = urequests.post(destination, data=payload, headers=headers)
        req.close()
        return req
