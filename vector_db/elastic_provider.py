import os
from typing import List

from langchain_core.documents import Document
from langchain_elasticsearch.vectorstores import ElasticsearchStore

from utils import get_required_env_var
from vector_db.db_provider import DBProvider


class ElasticProvider(DBProvider):
    """
    Elasticsearch-based vector DB provider.

    Required Environment Variables:
        - ELASTIC_URL: Full URL to the Elasticsearch cluster
        - ELASTIC_PASSWORD: Auth password

    Optional Environment Variables:
        - ELASTIC_INDEX: Index name (default: 'docs')
        - ELASTIC_USER: Auth username (default: 'elastic')
    """

    def __init__(self):
        super().__init__()

        url = get_required_env_var("ELASTIC_URL")
        password = get_required_env_var("ELASTIC_PASSWORD")
        index = os.getenv("ELASTIC_INDEX", "docs")
        user = os.getenv("ELASTIC_USER", "elastic")

        self.db = ElasticsearchStore(
            embedding=self.embeddings,
            es_url=url,
            es_user=user,
            es_password=password,
            index_name=index,
        )

    def add_documents(self, docs: List[Document]) -> None:
        self.db.add_documents(docs)
