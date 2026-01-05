"""FastAPI/uvicorn server that accepts plain text or JSON and returns a string."""

import json
from typing import Any, Callable, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse

from log.logger import get_logger

logger = get_logger(__name__)

MessageProcessor = Callable[[str, Dict[str, Any]], str]


def _parse_body(body: bytes, content_type: str) -> str:
    """Decode request body as text, falling back from JSON to raw text."""
    if not body:
        return ''

    if 'application/json' in content_type:
        try:
            payload = json.loads(body.decode('utf-8'))
            if isinstance(payload, str):
                return payload
            return json.dumps(payload, ensure_ascii=False)
        except json.JSONDecodeError:
            return body.decode('utf-8', errors='replace')

    return body.decode('utf-8', errors='replace')


def create_app(message_processor: Optional[MessageProcessor] = None) -> FastAPI:
    """Build FastAPI app with injectable message processor."""
    processor = message_processor or (lambda message, metadata: message)
    app = FastAPI()

    @app.get('/', response_class=PlainTextResponse)
    async def health() -> str:
        return 'Server is running. Send a POST with plain text or JSON.\n'

    @app.post('/', response_class=PlainTextResponse)
    async def handle(request: Request) -> str:
        raw_body = await request.body()
        content_type = request.headers.get('content-type', '')
        message = _parse_body(raw_body, content_type)
        metadata = {'path': request.url.path, 'headers': dict(request.headers)}

        try:
            return processor(message, metadata)
        except Exception as exc:  # pragma: no cover - defensive guard
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    logger.info('FastAPI server started')

    return app


def run_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    message_processor: Optional[MessageProcessor] = None,
) -> None:
    """Start uvicorn with the provided processor."""
    app = create_app(message_processor)
    uvicorn.run(app, host=host, port=port)
