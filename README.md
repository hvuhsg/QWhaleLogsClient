# QWhaleLogsClient
## QWhaleLogs client lib for saving logs in remote service

### Install
```shell script
$> pip install qwhale-logs-client
```

### Get token
Go to https://logs.qwhale.ml/provider/login
After the login go to https://logs.qwhale.ml/api/token

### Logging example
```python
import logging
from qwhale_logs_client import QWhaleLogsHandler

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SimpleOne")
logger.addHandler(QWhaleLogsHandler(token="<YOUR_TOKEN>", batch_site=1))  # Add our logs handler
# The batch site is determine how many logs to send in one request
# For fewer sizes more requests are made (default to 100)

logger.info("Some log") # Normal use
# Now your logs are sent to the QWhaleLogsService
```

### Loguru example (Recommended)
```python
from loguru import logger
from qwhale_logs_client import QWhaleLogsHandler

logger.add(QWhaleLogsHandler(token="<You'r-Token>", batch_site=1))
# The batch site is determine how many logs to send in one request
# For fewer sizes more requests are made (default to 100)

logger.info("Some log") # normal use
# Now your logs are sent to the QWhaleLogsService
```