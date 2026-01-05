from typing import Dict, Any
from dataclasses import dataclass, field
import os

from log.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ChatDeepSeekLLMProvider:
    config: Dict[str, Any] = field(default_factory=lambda: 
        {
            'llm': {
                'provider': 'deepseek', 
                'config': {
                    'model': 'deepseek-chat',
                    'temperature': 0.2,
                    'max_tokens': 2000,
                    'top_p': 1.0
                }
            }
        })
    
    base_url: str = 'https://api.deepseek.com'
    
    def __post_init__(self):
        self._log_warnings()
        self.chat_llm_api_key = os.environ.get('CHAT_LLM_API_KEY')
    
    def _log_warnings(self):
        if os.environ.get('CHAT_LLM_API_KEY') is None:
            logger.warning('Chat LLM API key not found. Please set the CHAT_LLM_API_KEY environment variable.')
            
    