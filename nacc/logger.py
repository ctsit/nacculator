import logging
import sys
from report_handler.report_handler import ReportHandler


def configure_logging(config, handlers: list[logging.Handler] = []):
    fmt = '%(asctime)s  %(levelname)-9s  %(message)s'

    logging.basicConfig(level=logging.DEBUG, format=fmt,
                        filename="logs.log")
    # if config.quiet:
    #     # Do not write logs to console; normal output still goes to stdout.
    #     return

    console = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(fmt)
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)
    # if config.verbose:
    #     # Increase verbosity if the "--verbose" flag was specified.
    #     console.setLevel(logging.DEBUG)
    # else:
    #     console.setLevel(logging.INFO)

    # Gets the root logger and any config changes here affects logging across the code base
    logger = logging.getLogger()

    logger.addHandler(console)

    for handler in handlers:
        logger.addHandler(handler)
