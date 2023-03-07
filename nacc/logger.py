from python_db_logger.db_logger import DBLogger
from python_db_logger.connection_helper import ConnectionHelper
import logging

db_logger: DBLogger = DBLogger(
    logging.getLogger(('')),
    ConnectionHelper(dot_env_file='.env')
)
