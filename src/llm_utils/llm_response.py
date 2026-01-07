from typing import Dict, Any
from time import perf_counter
import os
from collections import deque

from mem0 import Memory

from log.logger import get_logger
from environment import Config
from .prompt_example import USER_PROMPT, SYSTEM_PROMPT
from configs.chat_llm_providers import *

logger = get_logger(__name__)


class Responser:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        # Устанавливаем фиктивный OPENAI_API_KEY, если он не установлен или пустой
        # Это нужно, так как mem0 требует api_key для OpenAI-совместимого клиента, даже для локального TEI
        # Фиктивный ключ не будет использоваться, так как запросы идут на локальный TEI сервер через base_url
        openai_key = os.environ.get('OPENAI_API_KEY', '').strip()
        if not openai_key:
            os.environ['OPENAI_API_KEY'] = 'not-needed-for-local-tei'
            logger.info('Set dummy OPENAI_API_KEY for local TEI embeddings (not used for local server)')
        
        self.mem0_cfg = {
            'vector_store': cfg.MEM0.vector_store.config,
            'llm': cfg.MEM0.llm.config['llm'],
            'embedder': cfg.MEM0.embedder.config['embedder'],
            'reranker': cfg.MEM0.reranker.config['reranker']
        }
        
        self.memory = Memory.from_config(self.mem0_cfg)
        self.search_top_k = int(os.environ.get('MEMORY_SEARCH_TOP_K', 5))
        self.search_score_threshold = float(os.environ.get('MEMORY_SEARCH_SCORE_THRESHOLD', 0.2))
        self.max_context_chars = int(os.environ.get('MEMORY_CONTEXT_MAX_CHARS', 2000))
        self.default_user_id = os.environ.get('MEMORY_DEFAULT_USER_ID', 'default')
        self.default_session_id = os.environ.get('MEMORY_DEFAULT_SESSION_ID', 'default_session')
        self.max_history_messages = int(os.environ.get('MEMORY_TOP_K_LAST_MESSAGES', 3))
        self.recent_messages: Dict[str, deque] = {}
        # logger.info(self.CFG.OPENAI_API_KEY)
        # self.openai_client = OpenAI(api_key=self.CFG.OPENAI_API_KEY)
        self.chat_client = self._define_chat_client()
        
        
    def get_response(self, prompt: str, metadata: Dict[str, Any]) -> str | None:
        if self.chat_client is None:
            return ''
        user_id, session_id = self._resolve_ids(metadata)
        memory_context = ''
        mem_metadata = {'session_id': session_id, **(metadata or {})}
        recent_dialog = self._get_recent_history(user_id, session_id)
        search_t0 = perf_counter()

        try:
            search_results = self.memory.search(prompt, user_id=user_id)
            logger.info('Mem0 search results: %s', search_results)

            items = []
            if isinstance(search_results, dict):
                items = search_results.get('results') or search_results.get('data') or []
            elif isinstance(search_results, list):
                items = search_results

            items = list(items) if items else []

            if not items and user_id != self.default_user_id:
                fallback_results = self.memory.search(prompt, user_id=self.default_user_id)
                logger.info('Mem0 fallback search results: %s', fallback_results)
                if isinstance(fallback_results, dict):
                    items = fallback_results.get('results') or fallback_results.get('data') or []
                elif isinstance(fallback_results, list):
                    items = fallback_results or []
                else:
                    items = []

            if items:
                memory_context = self._build_context(items)
        except Exception as mem_err:
            logger.warning('Mem0 search failed: %s', mem_err, exc_info=True)
        search_t1 = perf_counter()

        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
        ]
        if recent_dialog:
            messages.extend(recent_dialog)
        if memory_context:
            messages.append(
                {
                    'role': 'system',
                    'content': f'--- CONTEXT START ---\n{memory_context}\n--- CONTEXT END ---',
                }
            )
        messages.append({'role': 'user', 'content': prompt})

        logger.info(
            'Chat prompt (no system): history=%s, context=%s, user=%s',
            recent_dialog,
            memory_context,
            prompt,
        )

        try:
            response_t0 = perf_counter()
            response = self.chat_client.chat.completions.create(
                model=self.cfg.CHAT_LLM.config['llm']['config']['model'],
                messages=messages
            )
            logger.info(response)
            response_content = response.choices[0].message.content
            response_t1 = perf_counter()
            logger.info(response_content)
            logger.info(
                'Timings: search=%.2f sec, chat=%.2f sec',
                search_t1 - search_t0,
                response_t1 - response_t0,
            )

            try:
                save_t0 = perf_counter()
                dialog_pair = [
                    {'role': 'user', 'content': prompt},
                    {'role': 'assistant', 'content': response_content},
                ]
                self.memory.add(dialog_pair, user_id=user_id, metadata={'role': 'conversation', **mem_metadata})
                self._remember_recent_history(user_id, session_id, dialog_pair)
                save_t1 = perf_counter()
                logger.info('Save time: %.2f sec', save_t1 - save_t0)
            except Exception as mem_add_err:
                logger.warning('Mem0 add failed: %s', mem_add_err, exc_info=True)

            return response_content
        except Exception as e:
            logger.error(f'Failed to get response from OpenAI: {e}', exc_info=True)
            return ''

    def _format_memory_context(self, items: list[Dict[str, Any]]) -> str:
        if not items:
            return ''

        lines: list[str] = []
        total_len = 0
        for item in items:
            content = item.get('content', '').replace('\n', ' ').strip()
            if not content:
                continue

            score = item.get('score')
            score_str = f'{score:.2f}' if isinstance(score, (int, float)) else 'n/a'

            meta = item.get('metadata') or {}
            role = meta.get('role') or meta.get('source') or 'mem0'
            line = f'- [score {score_str}][role {role}] {content}'
            projected_len = total_len + len(line)

            lines.append(line)
            total_len = projected_len

            if total_len >= self.max_context_chars:
                break

        context_text = '\n'.join(lines)
        return context_text[: self.max_context_chars]

    def _build_context(self, items: list[Any]) -> str:
        sorted_items = sorted(
            [it for it in items if isinstance(it, dict)],
            key=lambda x: self._score_value(x),
            reverse=True,
        )
        logger.info(
            'Mem0 candidates (sorted): %s',
            [
                {
                    'score': it.get('score'),
                    'rerank_score': it.get('rerank_score'),
                    'content': (it.get('memory') or it.get('content') or '')[:80],
                }
                for it in sorted_items
            ],
        )

        unique_chunks = set()
        filtered_chunks = []
        top_k_items = sorted_items[: self.search_top_k]

        for item in top_k_items:
            score = item.get('score')
            content = item.get('memory') or item.get('content') or ''
            if not content:
                continue
            content = content.strip()
            if content in unique_chunks:
                continue
            if score is not None and score < self.search_score_threshold:
                continue

            unique_chunks.add(content)
            filtered_chunks.append(
                {
                    'content': content,
                    'score': score,
                    'metadata': item.get('metadata') or {},
                }
            )

        if not filtered_chunks and top_k_items:
            best = top_k_items[0]
            content = (best.get('memory') or best.get('content') or '').strip()
            filtered_chunks.append(
                {
                    'content': content,
                    'score': best.get('score'),
                    'metadata': best.get('metadata') or {},
                }
            )
            logger.info('Mem0: no items passed threshold, used top-1 fallback')

        return self._format_memory_context(filtered_chunks)

    def _score_value(self, item: Dict[str, Any]) -> float:
        rerank = item.get('rerank_score')
        score = item.get('score')
        if rerank is not None:
            try:
                return float(rerank)
            except (TypeError, ValueError):
                pass
        if score is not None:
            try:
                return float(score)
            except (TypeError, ValueError):
                pass
        return 0.0

    def _resolve_ids(self, metadata: Dict[str, Any] | None) -> tuple[str, str]:
        user_id = self.default_user_id
        session_id = self.default_session_id

        if metadata:
            user_id = str(metadata.get('user_id', user_id))
            session_id = str(metadata.get('session_id', session_id))

            headers = metadata.get('headers') or {}
            for key, value in headers.items():
                key_l = str(key).lower()
                if key_l == 'x-user-id':
                    user_id = str(value)
                if key_l == 'x-session-id':
                    session_id = str(value)

        return user_id, session_id

    def _history_key(self, user_id: str, session_id: str) -> str:
        return f'{user_id}:{session_id}'

    def _get_recent_history(self, user_id: str, session_id: str) -> list[Dict[str, str]]:
        key = self._history_key(user_id, session_id)
        history = self.recent_messages.get(key)
        if not history:
            return []
        return list(history)

    def _remember_recent_history(self, user_id: str, session_id: str, dialog_pair: list[Dict[str, str]]) -> None:
        key = self._history_key(user_id, session_id)
        if key not in self.recent_messages:
            self.recent_messages[key] = deque(maxlen=self.max_history_messages * 2)
        self.recent_messages[key].extend(dialog_pair[-(self.max_history_messages * 2):])
    
    def _define_chat_client(self):
        if isinstance(self.cfg.CHAT_LLM, ChatDeepSeekLLMProvider):
            from openai import OpenAI
            chat_client = OpenAI(
                api_key=self.cfg.CHAT_LLM.chat_llm_api_key,
                base_url=self.cfg.CHAT_LLM.base_url
            )
            return chat_client
        elif isinstance(self.cfg.CHAT_LLM, ChatOpenaiLLMProvider):
            from openai import OpenAI
            chat_client = OpenAI(
                api_key=self.cfg.CHAT_LLM.chat_llm_api_key,
            )
            return chat_client
        
        logger.error(f'Unknown chat LLM provider: {self.cfg.CHAT_LLM.__name__}')
        return