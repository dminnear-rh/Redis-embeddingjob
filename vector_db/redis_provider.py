import logging
import os
from typing import List

import redis
from langchain_community.vectorstores.redis import Redis as RedisVectorStore
from langchain_core.documents import Document

from utils import get_required_env_var
from vector_db.db_provider import DBProvider

logger = logging.getLogger(__name__)


class RedisProvider(DBProvider):
    """
    Redis-based vector DB provider using RediSearch.

    Required Environment Variables:
        - REDIS_URL: Redis connection string (e.g. redis://localhost:6379)

    Optional Environment Variables:
        - REDIS_INDEX: RediSearch index name (default: 'docs')
        - REDIS_SCHEMA: Path to schema file for RediSearch index (default: 'redis_schema.yaml')
    """

    def __init__(self):
        super().__init__()

        self.url = get_required_env_var("REDIS_URL")
        self.index = os.getenv("REDIS_INDEX", "docs")
        self.schema = os.getenv("REDIS_SCHEMA", "redis_schema.yaml")

        try:
            self.redis_client = redis.from_url(self.url)
            # Proactively test the connection
            self.redis_client.ping()
        except Exception as e:
            logger.exception("Failed to connect to Redis at %s", self.url)
            raise

        # Determine whether to load from existing index or create a new one
        if self._index_exists():
            logger.info("Loading existing Redis index: %s", self.index)
            self.db = RedisVectorStore.from_existing_index(
                embedding=self.embeddings,
                redis_url=self.url,
                index_name=self.index,
                schema=self.schema,
            )
        else:
            logger.info("Creating new Redis index: %s", self.index)
            self.db = RedisVectorStore.from_documents(
                documents=[],  # Will be added later
                embedding=self.embeddings,
                redis_url=self.url,
                index_name=self.index,
            )
            logger.info("Writing Redis schema to: %s", self.schema)
            self.db.write_schema(self.schema)

    def _index_exists(self) -> bool:
        try:
            self.redis_client.ft(self.index).info()
            return True
        except Exception:
            return False

    def add_documents(self, docs: List[Document]) -> None:
        self.db.add_documents(docs)
