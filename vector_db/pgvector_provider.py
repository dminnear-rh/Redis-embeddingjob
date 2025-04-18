from typing import List

from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document

from utils import get_required_env_var
from vector_db.db_provider import DBProvider


class PGVectorProvider(DBProvider):
    """
    PostgreSQL PGVector-based vector DB provider.

    Required Environment Variables:
        - PGVECTOR_URL: PostgreSQL connection string
        - PGVECTOR_COLLECTION_NAME: Table or collection name in the database
    """

    def __init__(self):
        super().__init__()

        url = get_required_env_var("PGVECTOR_URL")
        collection_name = get_required_env_var("PGVECTOR_COLLECTION_NAME")

        self.db = PGVector(
            connection_string=url,
            collection_name=collection_name,
            embedding_function=self.embeddings,
        )

    def add_documents(self, docs: List[Document]) -> None:
        # Sanitize null characters (PG doesn't accept them)
        for doc in docs:
            doc.page_content = doc.page_content.replace("\x00", "")
        self.db.add_documents(docs)
