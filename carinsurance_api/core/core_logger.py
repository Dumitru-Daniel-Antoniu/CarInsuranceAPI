import logging
import structlog
import sys

from carinsurance_api.core.config import Settings


configuration = Settings()

env = "dev" if configuration.log_level.upper() == "DEBUG" else "prod"
log_level = configuration.log_level.upper()

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=getattr(logging, log_level)
)

if env == "prod":
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer()
    ]
else:
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.dev.ConsoleRenderer()
    ]

structlog.configure(
    processors=processors,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
