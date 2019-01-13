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

    def getRequest(self,destination,headers,url_params):
        #Form url:
        rootURI = destination+"?"

        for param in url_params:
            rootURI = rootURI+param+"="+url_params[param]+"&"

        uri = rootURI
        greq = urequests.get(rootURI,headers = headers)