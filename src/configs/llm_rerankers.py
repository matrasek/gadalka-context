from typing import Dict, Any
from dataclasses import dataclass, field
import os

from log.logger import get_logger

logger = get_logger(__name__)


@dataclass
class RerankerDeepSeekLLMProvider:
    config: Dict[str, Any] = field(default_factory=lambda: 
        {
            'reranker':{
                'provider': 'llm_reranker',
                'config': {
                    'llm': {
                        'provider': 'deepseek', 
                        'config': {
                            'model': 'deepseek-chat',
                            'api_key': os.environ.get('RERANKER_API_KEY', ''),
                            'temperature': 0.0,
                            'base_url': 'https://api.deepseek.com',
                            
                        }
                    }
                }
            }
        })
        
    def __post_init__(self):
        self._log_warnings()
    
    def _log_warnings(self):
        if os.environ.get('RERANKER_API_KEY') is None:
            logger.warning('Reranker API key not found. Please set the RERANKER_API_KEY environment variable.')
            
    