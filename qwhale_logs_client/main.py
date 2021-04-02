from concurrent.futures.thread import ThreadPoolExecutor
from json import dumps
from logging import Handler, LogRecord
from urllib.parse import urljoin

import requests

__all__ = ["QWhaleLogsHandler"]

SERVICE_URL = "https://logs.qwhale.ml/"


class QWhaleLogsHandler(Handler):
    def __init__(self, token: str, batch_site: int = 100, timeout: float = 7.5):
        self.token = token
        self.logs = []
        self.batch = None
        self.batch_size = batch_site
        self.timeout = timeout
        self.executor = ThreadPoolExecutor(max_workers=5)
        super().__init__()

    def __upload(self):
        payload = {"token": self.token}
        try:
            requests.put(
                urljoin(SERVICE_URL, "/api/logs"),
                params=payload,
                data=dumps({"logs": self.batch}),
                timeout=self.timeout,
            )
        except (ConnectionError, ValueError):
            pass

    def emit(self, record: LogRecord) -> None:
        self.logs.append(record.__dict__)
        if len(self.logs) >= self.batch_size:
            self.batch = self.logs.copy()
            self.logs.clear()
            self.executor.submit(self.__upload)

    def flush(self) -> None:
        self.__upload()

    def close(self) -> None:
        self.flush()
        super().close()
        self.executor.shutdown()
