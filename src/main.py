"""Main entrypoint with message processing logic for the FastAPI/uvicorn server."""

from typing import Any, Dict

from llm_utils.llm_response import Responser
from environment import Config
from app import create_app, run_server
from log.logger import get_logger

logger = get_logger(__name__)


def process_message(message: str, metadata: Dict[str, Any]) -> str:
    """Basic processor to adjust later."""
    logger.info(f'Received message: {message}, metadata: {metadata}')
    if not message:
        return 'No payload received.'
    return f'Echo: {message}'


# Expose app for `uvicorn main:app --reload`
app = create_app(process_message)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description='Run the simple text/JSON echo server (uvicorn).'
    )
    parser.add_argument('--host', default='0.0.0.0', help='Host interface to bind.')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on.')
    args = parser.parse_args()
    
    config = Config()
    
    responser = Responser(config)

    run_server(host=args.host, port=args.port, message_processor=responser.get_response)


if __name__ == "__main__":
    main()
