from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

import config
from vector_db.db_provider import DBProvider


class WebLoader:
    """
    Loads and processes documents from a list of web URLs, splits them into chunks,
    and stores them in a vector database.

    Chunking behavior is controlled by environment variables defined in the `config` module.

    Args:
        db_provider (DBProvider): The vector DB backend to which processed documents will be added.

    Example:
        >>> loader = WebLoader(my_db_provider)
        >>> urls = ["https://example.com/page1", "https://example.com/page2"]
        >>> loader.load(urls)
    """

    def __init__(self, db_provider: DBProvider):
        self.db_provider = db_provider
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP

    def load(self, urls: List[str]) -> None:
        """
        Loads documents from the provided URLs, splits them into chunks,
        and stores them into the vector database.

        Args:
            urls (List[str]): A list of URLs to load content from.
        """
        print("Loading web documents from the following URLs:")
        for url in urls:
            print(f" - {url}")

        docs = self._load_urls(urls)

        print(
            f"Splitting documents with chunk size '{self.chunk_size}' and chunk overlap '{self.chunk_overlap}'"
        )
        chunks = self._split_docs(docs)

        print("Adding document chunks to vector database")
        self.db_provider.add_documents(chunks)

    def _load_urls(self, urls: List[str]) -> List[Document]:
        loader = WebBaseLoader(urls)
        return loader.load()

    def _split_docs(self, docs: List[Document]) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return splitter.split_documents(docs)
