"""Simple mock client to interact with the FastAPI/uvicorn server."""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


def _request(
    method: str,
    url: str,
    data: Optional[bytes] = None,
    headers: Optional[Dict[str, str]] = None,
) -> str:
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read()
            return body.decode('utf-8', errors='replace')
    except urllib.error.HTTPError as exc:  # pragma: no cover - CLI helper
        return f'HTTP {exc.code}: {exc.reason}\n{exc.read().decode("utf-8", errors="replace")}'
    except urllib.error.URLError as exc:  # pragma: no cover - CLI helper
        return f'Connection error: {exc.reason}'


def send_text(base_url: str, text: str) -> str:
    return _request(
        'POST',
        base_url,
        data=text.encode('utf-8'),
        headers={'Content-Type': 'text/plain; charset=utf-8'},
    )


def send_json(base_url: str, payload: Any) -> str:
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    return _request(
        'POST',
        base_url,
        data=data,
        headers={'Content-Type': 'application/json'},
    )


def get_health(base_url: str) -> str:
    return _request('GET', base_url)


def main() -> None:
    parser = argparse.ArgumentParser(description='Mock client for the echo server.')
    parser.add_argument('--host', default='127.0.0.1', help='Server host.')
    parser.add_argument('--port', type=int, default=8000, help='Server port.')
    parser.add_argument(
        '--mode',
        choices=['text', 'json', 'health'],
        default='text',
        help='Request type to send.',
    )
    parser.add_argument(
        '--data',
        help='Text payload or JSON string (for --mode json).',
    )
    args = parser.parse_args()

    base_url = f'http://{args.host}:{args.port}/'

    if args.mode == 'health':
        print(get_health(base_url))
        return

    if args.mode == 'text':
        payload = args.data or 'hello'
        print(send_text(base_url, payload))
        return

    # json mode
    if args.data:
        try:
            payload_obj = json.loads(args.data)
        except json.JSONDecodeError:
            print('Invalid JSON in --data', file=sys.stderr)
            sys.exit(1)
    else:
        payload_obj = {'msg': 'hello'}

    print(send_json(base_url, payload_obj))


if __name__ == '__main__':
    main()
