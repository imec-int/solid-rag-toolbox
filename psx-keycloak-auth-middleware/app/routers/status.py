import uuid
import asyncio
import logging
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from app.utils.status_queue import get_status_queue

STREAM_DELAY = 0.2  # second(s)
RETRY_TIMEOUT = 15000  # milliseconds

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get('/status', tags=["auth status"])
async def message_stream(request: Request):
    def new_events():
        statusQueue = get_status_queue()
        return not statusQueue.empty()

    async def event_generator():
        logger.info('SSE listening started')
        statusQueue = get_status_queue()

        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_events():
                event = statusQueue.get()
                if (event):
                    print("sending event: ", event)
                    yield {
                        "event": "message",
                        "id": uuid.uuid4(),
                        "retry": RETRY_TIMEOUT,
                        "data": str(event)
                    }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())
