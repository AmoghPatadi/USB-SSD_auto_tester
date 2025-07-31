import logging

logger = logging.getLogger(__name__)

def setup_logging(level=logging.INFO):
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=level, format=format_str)
    logging.info("Logging is set up.")
