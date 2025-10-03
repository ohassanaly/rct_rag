import logging
import sys
from pathlib import Path

path = Path('.')
log_path = path / "rct_rag/test.log" #dev mode ; in deployment, logs are expected in sys.stdout

#get logger
logger = logging.getLogger("rct_rag")
logger.setLevel(logging.INFO)

#create formater
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
    )

#create handlers
stream_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)
file_handler = logging.FileHandler(log_path)

#set formatters
stream_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Route different levels appropriately for the production log handlers
stream_handler.addFilter(lambda record: record.levelno < logging.ERROR)
stderr_handler.addFilter(lambda record: record.levelno >= logging.ERROR)

#add handlers to the logger
logger.handlers = [stream_handler, stderr_handler, file_handler]


