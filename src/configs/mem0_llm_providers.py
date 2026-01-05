from typing import Dict, Any
from dataclasses import dataclass, field
import os

from log.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Mem0DeepSeekLLMProvider:
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
    
    def __post_init__(self):
        self._log_warnings()
    
    def _log_warnings(self):
        if os.environ.get('DEEPSEEK_API_KEY') is None:
            logger.warning('DeepSeek API key not found. Please set the DEEPSEEK_API_KEY environment variable.')
    