#!/usr/bin/env python

import logging
import os

import config
from loaders.pdf_loader import PDFLoader
from loaders.web_loader import WebLoader
from utils import get_required_env_var
from vector_db.db_type import DBType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create db_provider based on user-provided DB_TYPE env var
try:
    db_type = DBType.from_string(config.DB_TYPE)
    db_provider = db_type.get_provider_class()()
    logger.info(f"Using vector DB provider: %s", db_type.value)
except Exception as e:
    logger.exception("Failed to initialize DB provider.")
    raise

# Load documents from folder of PDF files
try:
    pdf_loader = PDFLoader(db_provider)
    pdf_folder = get_required_env_var("PDF_FOLDER")
    logger.info("Loading and embedding PDF documents from: %s", pdf_folder)
    pdf_loader.load(pdf_folder)
    logger.info("Finished processing PDF documents.")
except Exception as e:
    logger.exception("Error while processing PDF documents.")
    raise

# Load documents from web pages
try:
    web_loader = WebLoader(db_provider)
    logger.info("Loading and embedding web documents from configured URLs.")
    web_loader.load(config.WEB_URLS)
    logger.info("Finished processing web documents.")
except Exception as e:
    logger.exception("Error while processing web documents.")
    raise
