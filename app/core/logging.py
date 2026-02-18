import logging
import sys


def setup_logging(debug: bool = False) -> logging.Logger:
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger("ai_summarizer")


logger = setup_logging()
