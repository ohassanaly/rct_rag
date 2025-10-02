import logging
import sys

# from dotenv import load_dotenv
# import os

# from logtail import LogtailHandler #better stack

# load_dotenv()

from pathlib import Path

path = Path('.')
log_path = path / "rct_rag/test.log"

#get logger
logger = logging.getLogger()

#create formater
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
    )

#create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(log_path)
# better_stack_handler = LogtailHandler(source_token=os.getenv("better_stack_token"), host = os.getenv("better_stack_host"))

#set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

#add handlers to the logger
logger.handlers = [stream_handler, file_handler]

# logger.handlers = [stream_handler, file_handler, better_stack_handler]

#set log-level
logger.setLevel(logging.INFO)


#other experiments
# from loguru import logger
# from logtail import LogtailHandler #better stack


# from pathlib import Path

# # from dotenv import load_dotenv
# # import os
# # load_dotenv()

# # logger.remove(0)
# # better_stack_handler = LogtailHandler(source_token=os.getenv("better_stack_token"), host = os.getenv("better_stack_host"))
# # logger.add(sink = better_stack_handler, serialize = True, level="INFO") #serialize = True ignores formatting

# path = Path('.')
# log_path = path / "rct_rag/test.log"
# logger.add(sink = log_path, serialize = True, level="TRACE")
