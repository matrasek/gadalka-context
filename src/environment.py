from dataclasses import dataclass, field
import os


from configs.mem0_llm_providers import Mem0DeepSeekLLMProvider
from configs.chat_llm_providers import ChatDeepSeekLLMProvider
from configs.vector_stores import QdrantStore
from configs.tei_embedding_models import TEIDeepVkUserBgeM3
from configs.llm_rerankers import RerankerDeepSeekLLMProvider

@dataclass
class Mem0Config:
    llm: Mem0DeepSeekLLMProvider = field(default_factory=Mem0DeepSeekLLMProvider)
    vector_store: QdrantStore = field(default_factory=QdrantStore)
    embedder: TEIDeepVkUserBgeM3 = field(default_factory=TEIDeepVkUserBgeM3)
    reranker: RerankerDeepSeekLLMProvider = field(default_factory=RerankerDeepSeekLLMProvider)


@dataclass
class Config:
    CHAT_LLM: ChatDeepSeekLLMProvider = field(default_factory=ChatDeepSeekLLMProvider)
    MEM0: Mem0Config = field(default_factory=Mem0Config)
    