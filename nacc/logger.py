import logging
import sys
from report_handler.report_handler import ReportHandler

global report_handler


def configure_logging(config):
    fmt = '%(asctime)s  %(levelname)-9s  %(message)s'

    logging.basicConfig(level=logging.DEBUG, format=fmt,
                        filename=ReportHandler.prevent_overwrite(config.log))

    if config.quiet:
        # Do not write logs to console; normal output still goes to stdout.
        return

    console = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(fmt)
    console.setFormatter(formatter)
    if config.verbose:
        # Increase verbosity if the "--verbose" flag was specified.
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)

    global report_handler
    report_handler = ReportHandler()

    # Gets the root logger and any config changes here affects logging across the code base
    logger = logging.getLogger()

    logger.addHandler(console)
    logger.addHandler(report_handler)


if __name__ == "logger":
    configure_logging()

# from python_db_logger.db_logger import DBLogger
# from python_db_logger.connection_helper import ConnectionHelper
# import logging

# """
# Why a separate file? Since Python imports provide the same 
# reference of a module wherever imported, it is easier to create
# DBLogger in a separate file and import it everywhere. This way,
# we don't have to worry about creating and passing the dbLogger 
# instances from one file to another.
# """

# logging_instance = logging.getLogger('nacculator-db-logger')
# logging_instance.setLevel(logging.DEBUG)

# db_logger: DBLogger = DBLogger(
#     logging_instance,
#     ConnectionHelper(dot_env_file='.env').connect_to_mysql(),
#     write_to_prod=True
# )
