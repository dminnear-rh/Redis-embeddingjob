import json
from typing import Optional, List
import uuid
from langchain_sqlserver import SQLServer_VectorStore
from vector_db.db_provider import DBProvider
from langchain_core.documents import Document
import langchain_huggingface as hf
import os
import pyodbc


class SQLServerProvider(DBProvider):
    type = "SQLSERVER"

    def __init__(self) -> None:
        super().__init__()
        self.database = os.getenv("SQLSERVER_DB", "docs")
        self.connection_string = self._build_connection_string_from_env()
        self.table = self._get_required_env("SQLSERVER_TABLE")
        self.db: Optional[SQLServer_VectorStore] = None

        # Ensure the target DB exists before proceeding
        self._ensure_database_exists()

    @staticmethod
    def _get_required_env(key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} environment variable is required.")
        return value

    @classmethod
    def _build_connection_string_from_env(cls, override_db: Optional[str] = None) -> str:
        host = cls._get_required_env("SQLSERVER_HOST")
        port = cls._get_required_env("SQLSERVER_PORT")
        user = cls._get_required_env("SQLSERVER_USER")
        password = cls._get_required_env("SQLSERVER_PASSWORD")
        driver = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server")
        database = override_db if override_db else os.getenv("SQLSERVER_DB", "docs")

        return (
            f"Driver={{{driver}}};"
            f"Server={host},{port};"
            f"Database={database};"
            f"UID={user};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
            "Encrypt=no;"
        )

    def _ensure_database_exists(self) -> None:
        # Connect to the 'master' DB and try to create the target DB if it doesn't exist
        master_conn_str = self._build_connection_string_from_env(override_db="master")
        try:
            with pyodbc.connect(master_conn_str, autocommit=True) as conn:
                cursor = conn.cursor()
                cursor.execute(f"IF DB_ID('{self.database}') IS NULL CREATE DATABASE [{self.database}]")
                cursor.close()
        except Exception as e:
            raise RuntimeError(f"Failed to ensure database '{self.database}' exists: {e}")

    @classmethod
    def _get_type(cls) -> str:
        """Returns type of the db provider."""
        return cls.type

    def get_client(self) -> SQLServer_VectorStore:
        if self.db is None:
            self.db = SQLServer_VectorStore(
                connection_string=self.connection_string,
                embedding_function=self.get_embeddings(),
                table_name=self.table,
                embedding_length=768,
            )
        return self.db

    def add_documents(self, docs: List[Document]) -> None:
        texts = [doc.page_content for doc in docs]
        metadatas = [doc.metadata for doc in docs]
        ids = [str(uuid.uuid4()) for _ in docs]

        self.get_client().add_texts(texts, metadatas, ids=ids)
