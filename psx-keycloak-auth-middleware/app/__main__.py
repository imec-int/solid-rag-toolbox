import signal
import sys
import logging

from app.routers import auth_v2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import load
from .routers import common, auth, status

config = load.Settings()
config.setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.allowOrigins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(common.router)
app.include_router(auth.router)
app.include_router(status.router)

app.include_router(auth_v2.router)


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
