import logging


def configure_logging(level: logging):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)-7s: %(lineno)-3s %(levelname)-7s - %(message)s",
    )
