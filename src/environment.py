from dataclasses import dataclass, field
import os


from configs.chat_llm_providers import ChatDeepSeekLLMProvider, ChatOpenaiLLMProvider
from configs.mem0_llm_providers import Mem0DeepSeekLLMProvider
from configs.vector_stores import QdrantStore
from configs.tei_embedding_models import TEIDeepVkUserBgeM3
from configs.llm_rerankers import RerankerDeepSeekLLMProvider

from log.logger import get_logger

logger = get_logger(__name__)

@dataclass
class Mem0Config:
    llm: Mem0DeepSeekLLMProvider = field(default_factory=Mem0DeepSeekLLMProvider)
    vector_store: QdrantStore = field(default_factory=QdrantStore)
    embedder: TEIDeepVkUserBgeM3 = field(default_factory=TEIDeepVkUserBgeM3)
    reranker: RerankerDeepSeekLLMProvider = field(default_factory=RerankerDeepSeekLLMProvider)


@dataclass
class Config:
    CHAT_LLM: ChatDeepSeekLLMProvider | ChatOpenaiLLMProvider = field(default_factory=ChatDeepSeekLLMProvider)
    MEM0: Mem0Config = field(default_factory=Mem0Config)
    
    def __post_init__(self):
        # CHAT_LLM REDEFINE
        if os.environ.get('CHAT_LLM_PROVIDER') is None:
            logger.error('CHAT_LLM_PROVIDER environment variable not found. Please set the CHAT_LLM_PROVIDER environment variable.')
            raise ValueError('CHAT_LLM_PROVIDER environment variable not found. Please set the CHAT_LLM_PROVIDER environment variable.')
        else:
            chat_llm_map = {
                'deepseek': ChatDeepSeekLLMProvider,
                'openai': ChatOpenaiLLMProvider
            }
            try:
                self.CHAT_LLM = chat_llm_map[str(os.environ.get('CHAT_LLM_PROVIDER'))]
            except KeyError:
                logger.error(f'Unknown CHAT_LLM_PROVIDER: {os.environ.get("CHAT_LLM_PROVIDER")}')
                raise ValueError(f'Unknown CHAT_LLM_PROVIDER: {os.environ.get("CHAT_LLM_PROVIDER")}')
            
    