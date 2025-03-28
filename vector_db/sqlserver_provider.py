from typing import Optional, List
from langchain_sqlserver import SQLServer_VectorStore
from vector_db.db_provider import DBProvider
from langchain_core.documents import Document
import os


class SQLServerProvider(DBProvider):
    type = "SQLSERVER"

    def __init__(self) -> None:
        super().__init__()
        self.connection_string = self._build_connection_string_from_env()
        self.table = self._get_required_env("SQLSERVER_TABLE")
        self.db: Optional[SQLServer_VectorStore] = None

    @staticmethod
    def _get_required_env(key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} environment variable is required.")
        return value

    @classmethod
    def _build_connection_string_from_env(cls) -> str:
        host = cls._get_required_env("SQLSERVER_HOST")
        port = cls._get_required_env("SQLSERVER_PORT")
        user = cls._get_required_env("SQLSERVER_USER")
        password = cls._get_required_env("SQLSERVER_PASSWORD")
        driver = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server")
        database = os.getenv("SQLSERVER_DB", "docs")

        return (
            f"Driver={{{driver}}};"
            f"Server={host},{port};"
            f"Database={database};"
            f"UID={user};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
        )

    @classmethod
    def _get_type(cls) -> str:
        """Returns type of the db provider."""
        return cls.type

    def get_client(self) -> SQLServer_VectorStore:
        if self.db is None:
            self.db = SQLServer_VectorStore(
                connection_string=self.connection_string,
                embedding_function=self.get_embeddings(),
                table_name=self.table
            )
        return self.db

    def add_documents(self, docs: List[Document]) -> None:
        self.get_client().add_documents(docs)
