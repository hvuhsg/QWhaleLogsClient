from traceback import format_exc
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from json import dumps
from logging import Handler, LogRecord
from urllib.parse import urljoin

try:
    import loguru

    HAS_LOGURU = True
except ImportError:
    HAS_LOGURU = False

import requests

__all__ = ["QWhaleLogsHandler", "init"]

SERVICE_URL = "https://logs.qwhale.ml/"


class QWhaleLogsHandler(Handler):
    def __init__(
        self,
        token: str,
        batch_size: int = 100,
        timeout: float = 7.5,
        project: str = "main",
        **kwargs
    ):
        self.token = token
        self.project = project
        self.logs = []
        self.batch = None
        self.batch_size = batch_size
        self.timeout = timeout
        self.executor = ThreadPoolExecutor(max_workers=5)
        super().__init__()

    def __upload(self):
        payload = {"token": self.token, "project": self.project}
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
        record_msg = None
        record_exc_info = None
        if not isinstance(record.msg, str):
            record_msg = str(record.msg)
        if record.exc_info and (not isinstance(record.exc_info, str)):
            record_exc_info = format_exc(limit=20)

        record_dict = record.__dict__.copy()
        if record_msg is not None:
            record_dict["msg"] = record_msg
        if record_exc_info is not None:
            record_dict["exc_info"] = record_exc_info

        self.logs.append(record_dict)
        if len(self.logs) >= self.batch_size:
            self.batch = self.logs.copy()
            self.logs.clear()
            self.executor.submit(self.__upload)

    def flush(self) -> None:
        self.batch = self.logs.copy()
        self.logs.clear()
        self.__upload()

    def close(self) -> None:
        self.flush()
        super().close()
        self.executor.shutdown()


def init(token: str, batch_size: int = 100, project: str = "main", **kwargs) -> None:
    """

    :param token: service token (For Authentication)
    :param batch_size: (How much to send in one batch)
    :param project: The project name for multiple project on the same token
    :param kwargs: timeout and more ...
    :return: None
    """
    handler = QWhaleLogsHandler(token, batch_size=batch_size, project=project, **kwargs)
    if HAS_LOGURU:
        loguru.logger.add(handler)
    logging.root.addHandler(handler)
    for name, logger in logging.Logger.manager.loggerDict.items():
        if isinstance(logger, logging.Logger):
            logger.addHandler(handler)
