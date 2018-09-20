import numpy as np
import requests
import warnings

from keras.callbacks import Callback

class MambasCallback(Callback):

    def __init__(self, id_project, root="http://localhost:8080", proxies={}, custom_metrics=[]):
        super(MambasCallback, self).__init__()
        self.id_project = id_project
        self.root = root
        self.proxies = proxies
        self.custom_metrics = custom_metrics
        self.id_session = None

    def on_train_begin(self, logs=None):
        path = "{}/projects/{}/sessions".format(self.root, self.id_project)
        answer = self.__send("post", path)

        message = {}
        message["start"] = "True"

        if answer is not None:
            self.id_session = answer["id_session"]
            path = "{}/projects/{}/sessions/{}".format(self.root, self.id_project, self.id_session)
            self.__send("put", path, message)
        else:
            warnings.warn("Warning: Could not set session id")

    def on_epoch_end(self, epoch, logs=None):
        message = {}
        message["epoch"] = epoch
        
        metrics = {}
        for k, v in logs.items():
            if isinstance(v, (np.ndarray, np.generic)):
                metrics[k] = v.item()
            else:
                metrics[k] = v
        for c in self.custom_metrics:
            metrics[c.__name__] = c(epoch=epoch)   
        message["metrics"] = metrics

        if self.id_session is not None:
            path = "{}/projects/{}/sessions/{}/epochs".format(self.root, self.id_project, self.id_session)
            self.__send("post", path, message)
        else:
            warnings.warn("Warning: Could not send epoch information because session id is not set")

    def on_train_end(self, logs=None):
        message = {}
        message["end"] = "True"

        if self.id_session is not None:
            path = "{}/projects/{}/sessions/{}".format(self.root, self.id_project, self.id_session)
            self.__send("put", path, message)
        else:
            warnings.warn("Warning: Could not send epoch information because session id is not set")
    
    def __send(self, method, path, message=None):
        answer = None

        try:
            if method == "put":
                r = requests.put(path, proxies=self.proxies) if message is None else requests.put(path, proxies=self.proxies, json=message)
            elif method == "post":
                r = requests.post(path, proxies=self.proxies) if message is None else requests.post(path, proxies=self.proxies, json=message)
            else:
                raise ValueError("HTTP method {} is not available".format(method))
            
            if r.status_code == 200:
                if r.text:
                    answer = r.json()
            else:
                warnings.warn("Warning: Mambas server answered with HTTP status code {}".format(r.status_code))

        except requests.exceptions.RequestException:
            warnings.warn("Warning: Could not reach Mambas server at {}".format(str(self.root)))

        return answer
