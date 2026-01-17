import json
import os
from typing import Any, Dict, List

import redis  # type: ignore

from log.logger import get_logger

logger = get_logger(__name__)


class RedisMemory:
    def __init__(
        self,
        url: str | None = None,
        host: str | None = None,
        port: int | None = None,
        db: int | None = None,
        username: str | None = None,
        password: str | None = None,
        window_size: int | None = None,
    ):
        self.url = url or os.environ.get('REDIS_URL') or os.environ.get('REDIS_PUBLIC_URL')
        self.host = host or os.environ.get('REDIS_HOST') or os.environ.get('REDISHOST') or 'redis'
        self.port = port if port is not None else int(
            os.environ.get('REDIS_PORT') or os.environ.get('REDISPORT') or 6379
        )
        self.db = db if db is not None else int(os.environ.get('REDIS_DB') or 0)
        self.username = username or os.environ.get('REDIS_USERNAME') or os.environ.get('REDISUSER')
        self.password = password or os.environ.get('REDIS_PASSWORD') or os.environ.get('REDISPASSWORD')
        self.window_size = (
            window_size if window_size is not None else int(os.environ.get('CHAT_HISTORY_WINDOW_SIZE') or 10)
        )
        self._client: redis.Redis | None = None

        self.current_planet_position_key = os.environ.get('CURRENT_PLANET_POSITION_KEY', 'astro:positions:current')

    def _get_client(self) -> redis.Redis:
        if self._client is None:
            if self.url:
                logger.info('Connecting to Redis via URL %s', self.url)
                self._client = redis.from_url(
                    self.url,
                    db=self.db,
                    decode_responses=True,
                )
            else:
                logger.info('Connecting to Redis host=%s port=%s db=%s', self.host, self.port, self.db)
                self._client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    username=self.username,
                    password=self.password,
                    decode_responses=True,
                )
        return self._client

    @staticmethod
    def _chat_key(chat_id: str) -> str:
        return f'chat:{chat_id}:messages'

    def add_message(self, chat_id: str, role: str, content: str) -> None:
        message = json.dumps({'role': role, 'content': content}, ensure_ascii=False)
        client = self._get_client()
        key = self._chat_key(chat_id)
        pipeline = client.pipeline()
        pipeline.rpush(key, message)
        pipeline.ltrim(key, -self.window_size, -1)
        pipeline.execute()
    
    def get_current_planet_position(self) -> str:
        client = self._get_client()
        raw_value = client.get(self.current_planet_position_key)
        if not raw_value:
            return ''

        if not isinstance(raw_value, str):
            raw_value = str(raw_value)

        try:
            payload: Any = json.loads(raw_value)
        except json.JSONDecodeError:
            logger.warning(
                'Failed to decode JSON for current planet positions key=%s raw=%s',
                self.current_planet_position_key,
                raw_value,
            )
            return raw_value.strip()

        formatted = self._format_planet_positions(payload)
        return formatted.strip()

    @staticmethod
    def _format_planet_positions(payload: Any) -> str:
        if isinstance(payload, dict):
            lines: List[str] = []
            for name, value in sorted(payload.items()):
                line = RedisMemory._format_planet_position_row(name, value)
                if line:
                    lines.append(line)
            return '\n'.join(lines)

        if isinstance(payload, list):
            lines: List[str] = []
            for entry in payload:
                if isinstance(entry, dict):
                    planet = entry.get('planet') or entry.get('name')
                    if planet:
                        entry_details = {
                            k: v for k, v in entry.items() if k not in {'planet', 'name'}
                        }
                        if entry_details:
                            lines.append(RedisMemory._format_planet_position_row(planet, entry_details))
                        else:
                            lines.append(planet)
                        continue
                normalized = RedisMemory._normalize_planet_position_value(entry)
                if normalized:
                    lines.append(normalized)
            return '\n'.join(lines)

        return RedisMemory._normalize_planet_position_value(payload)

    @staticmethod
    def _format_planet_position_row(name: str, value: Any) -> str:
        if not name:
            return RedisMemory._normalize_planet_position_value(value)

        if isinstance(value, dict):
            if not value:
                return name
            parts: List[str] = []
            for attr, attr_value in sorted(value.items()):
                part = RedisMemory._normalize_planet_position_value(attr_value)
                parts.append(f'{attr}: {part}')
            return f'{name}: ' + '; '.join(parts)

        if isinstance(value, list):
            items = ', '.join(RedisMemory._normalize_planet_position_value(item) for item in value)
            return f'{name}: [{items}]'

        normalized_value = RedisMemory._normalize_planet_position_value(value)
        return f'{name}: {normalized_value}' if normalized_value else name

    @staticmethod
    def _normalize_planet_position_value(value: Any) -> str:
        if value is None:
            return ''

        if isinstance(value, str):
            return value.strip()

        if isinstance(value, (int, float, bool)):
            return str(value)

        try:
            return json.dumps(value, ensure_ascii=False, separators=(',', ':'))
        except TypeError:
            return str(value)

    def get_last_messages(self, chat_id: str) -> List[Dict[str, str]]:
        client = self._get_client()
        key = self._chat_key(chat_id)
        raw_messages = client.lrange(key, -self.window_size, -1)
        messages: List[Dict[str, str]] = []

        for raw in raw_messages:
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict) and 'role' in parsed and 'content' in parsed:
                    messages.append({'role': parsed['role'], 'content': parsed['content']})
            except json.JSONDecodeError:
                logger.warning('Failed to decode redis message for chat_id=%s', chat_id)

        return messages

    def clear_history(self, chat_id: str) -> None:
        self._get_client().delete(self._chat_key(chat_id))

