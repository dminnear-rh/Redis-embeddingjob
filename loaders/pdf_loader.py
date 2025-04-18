from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document

import config
from vector_db.db_provider import DBProvider


class PDFLoader:
    """
    Loads and processes PDF files from a given directory and stores them into a vector database.

    Chunking behavior is controlled by environment variables defined in the `config` module.

    Args:
        db_provider (DBProvider): The vector DB backend to which processed documents will be added.

    Example:
        >>> loader = PDFLoader(my_db_provider)
        >>> loader.load("/path/to/pdf/folder")
    """

    def __init__(self, db_provider: DBProvider):
        self.db_provider = db_provider
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP

    def load(self, folder_path: str) -> None:
        """
        Loads all PDF documents from the specified folder, splits them into text chunks,
        and stores those chunks in the vector database.

        Args:
            folder_path (str): Absolute or relative path to the directory containing PDF files.
        """
        print(f"Loading PDFs from '{folder_path}'")
        docs = self._load_pdfs(folder_path)

        print(
            f"Splitting documents with chunk size '{self.chunk_size}' and overlap '{self.chunk_overlap}'"
        )
        chunks = self._split_docs(docs)

        print("Adding document chunks to vector database")
        self.db_provider.add_documents(chunks)

    def _load_pdfs(self, folder_path: str) -> List[Document]:
        loader = PyPDFDirectoryLoader(folder_path)
        return loader.load()

    def _split_docs(self, docs: List[Document]) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return splitter.split_documents(docs)
