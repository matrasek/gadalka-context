from typing import Dict, Any
from dataclasses import dataclass, field
import os

from log.logger import get_logger

logger = get_logger(__name__)


@dataclass
class QdrantStore:
    """
    http://localhost:6333/dashboard
    """
    config: Dict[str, Any] = field(default_factory=lambda: 
        {
            'provider': 'qdrant', 
            'config': {
                'host': 'localhost',
                'port': 6333,
                'collection_name': 'test-gadalka',
                'embedding_model_dims': 1024  # Размерность векторов для bge-m3
            }
        })
    