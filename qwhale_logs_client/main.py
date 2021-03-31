import requests
from json import dumps
from urllib.parse import urljoin
from logging import Handler, LogRecord

__all__ = ["QWhaleLogsHandler"]

SERVICE_URL = "https://logs.qwhale.ml/"


class QWhaleLogsHandler(Handler):
    def __init__(self, token: str, batch_site: int = 100):
        self.token = token
        self.logs = []
        self.batch = None
        self.batch_size = batch_site
        super().__init__()

    def __upload(self):
        payload = {"token": self.token}
        try:
            requests.put(urljoin(SERVICE_URL, f"/api/logs"), params=payload, data=dumps({"logs": self.batch}))
        except (ConnectionError, ValueError) as EX:
            pass

    def emit(self, record: LogRecord) -> None:
        self.logs.append(record.__dict__)
        if len(self.logs) >= self.batch_size:
            self.batch = self.logs.copy()
            self.logs.clear()
            self.__upload()
