import signal
import sys
import logging

from fastapi import FastAPI
from .config import load
from .routers import common, chunk


config = load.Settings()
config.setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(common.router)
app.include_router(chunk.router)


def shutdown_handler(signal, frame):
    logger.info("Received exit signal, shutting down gracefully...")
    sys.exit(0)


# Register the signal handlers
signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=config.port, log_level=config.logLevel.value.lower()
    )
