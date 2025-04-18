import logging
import os
from typing import List

import pyodbc
from langchain_core.documents import Document
from langchain_sqlserver import SQLServer_VectorStore

from utils import get_required_env_var
from vector_db.db_provider import DBProvider

logger = logging.getLogger(__name__)


class SQLServerProvider(DBProvider):
    """
    SQL Server-based vector DB provider using LangChain's SQLServer_VectorStore.

    Required Environment Variables:
        - SQLSERVER_HOST: Host of the SQL Server instance
        - SQLSERVER_PORT: Port number
        - SQLSERVER_USER: Database username
        - SQLSERVER_PASSWORD: Password
        - SQLSERVER_TABLE: Name of the table to store vectors

    Optional Environment Variables:
        - SQLSERVER_DB: Name of the database (default: 'docs')
        - SQLSERVER_DRIVER: ODBC driver name (default: 'ODBC Driver 18 for SQL Server')
    """

    def __init__(self) -> None:
        super().__init__()

        self.database = os.getenv("SQLSERVER_DB", "docs")
        self.table = get_required_env_var("SQLSERVER_TABLE")
        self.connection_string = self._build_connection_string(self.database)

        self._ensure_database_exists()
        self.db = SQLServer_VectorStore(
            connection_string=self.connection_string,
            embedding_function=self.embeddings,
            table_name=self.table,
            embedding_length=768,  # This should match the model used
        )

    def _build_connection_string(self, db_name: str) -> str:
        host = get_required_env_var("SQLSERVER_HOST")
        port = get_required_env_var("SQLSERVER_PORT")
        user = get_required_env_var("SQLSERVER_USER")
        password = get_required_env_var("SQLSERVER_PASSWORD")
        driver = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server")

        return (
            f"Driver={{{driver}}};"
            f"Server={host},{port};"
            f"Database={db_name};"
            f"UID={user};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
            "Encrypt=no;"
        )

    def _ensure_database_exists(self) -> None:
        master_conn_str = self._build_connection_string("master")
        try:
            with pyodbc.connect(master_conn_str, autocommit=True) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"IF DB_ID('{self.database}') IS NULL CREATE DATABASE [{self.database}]"
                )
                cursor.close()
        except Exception as e:
            logger.exception("Failed to ensure database '%s' exists", self.database)
            raise RuntimeError(
                f"Failed to ensure database '{self.database}' exists: {e}"
            )

    def add_documents(self, docs: List[Document]) -> None:
        self.db.add_documents(docs)
