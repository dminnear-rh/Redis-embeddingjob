from enum import Enum
from typing import Self, Type

from vector_db.db_provider import DBProvider
from vector_db.elastic_provider import ElasticProvider
from vector_db.pgvector_provider import PGVectorProvider
from vector_db.redis_provider import RedisProvider
from vector_db.sqlserver_provider import SQLServerProvider


class DBType(str, Enum):
    """
    Enum representing the supported types of vector database backends.

    Each type corresponds to a specific DBProvider subclass implementation.
    """

    REDIS = "REDIS"
    ELASTIC = "ELASTIC"
    PGVECTOR = "PGVECTOR"
    SQLSERVER = "SQLSERVER"

    @classmethod
    def from_string(cls, value: str) -> Self:
        """
        Convert a string to a DBType enum member.

        Args:
            value (str): The string representation of the DB type (case-insensitive).

        Returns:
            DBType: The matching DBType enum member.

        Raises:
            ValueError: If the provided string does not match any valid DBType.
        """
        try:
            return cls(value.strip().upper())
        except ValueError:
            valid_values = ", ".join([t.value for t in cls])
            raise ValueError(
                f"Invalid DB_TYPE '{value}'. Must be one of: {valid_values}"
            )

    def get_provider_class(self) -> Type["DBProvider"]:
        """
        Get the DBProvider subclass associated with this DBType.

        Returns:
            Type[DBProvider]: The class implementing the backend logic for this DB type.

        Raises:
            NotImplementedError: If no provider is defined for the given DBType.
        """
        if self == DBType.REDIS:
            return RedisProvider
        elif self == DBType.ELASTIC:
            return ElasticProvider
        elif self == DBType.PGVECTOR:
            return PGVectorProvider
        elif self == DBType.SQLSERVER:
            return SQLServerProvider
        else:
            raise NotImplementedError(f"No DBProvider available for DBType: {self}")
