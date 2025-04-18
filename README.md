# Document Embedding Job for OpenShift

This project provides a flexible, containerized embedding pipeline that loads documents from various sources (PDFs, web URLs, Git repositories) and stores their vector embeddings in a configured vector database.

It is designed to run as a Kubernetes job, specifically in **OpenShift** environments.

---

## 📦 Features

- ✅ Supports multiple vector DB backends: Redis, Elasticsearch, PGVector, SQL Server
- ✅ Loads documents from:
  - PDFs stored in a Git repo
  - Predefined or configurable web URLs
- ✅ Uses `sentence-transformers` for embedding
- ✅ Pluggable backend architecture via `DB_TYPE` env var
- ✅ Hugging Face model download caching supported
- ✅ Works with OpenShift-compatible UBI container

---

## 🚀 Usage

### Environment Variables

| Name                  | Required | Description                                                      |
|-----------------------|----------|------------------------------------------------------------------|
| `DOC_GIT_REPO`        | ✅       | URL to a Git repo containing the PDF documents                  |
| `DOC_LOCATION`        | ❌       | Relative path inside the repo to the PDF folder (default: repo root) |
| `TEMP_DIR`            | ❌       | Directory where the repo is cloned (default: `/tmp`)            |
| `DB_TYPE`             | ❌       | One of: `REDIS`, `ELASTIC`, `PGVECTOR`, `SQLSERVER` (default: `REDIS`) |
| `WEB_URLS`            | ❌       | Comma-separated list of URLs to embed (overrides built-in list) |
| `CHUNK_SIZE`          | ❌       | Size of document chunks (default: `1024`)                       |
| `CHUNK_OVERLAP`       | ❌       | Chunk overlap in characters (default: `40`)                     |

Each DB type also requires its own env vars (e.g., `REDIS_URL`, `ELASTIC_URL`, etc.). See the source under [`vector_db/`](./vector_db) for specifics.

---

### Building the Container

```bash
podman build -t embed-job .
```

### Running the Job

```bash
podman run --rm \
  -e DOC_GIT_REPO=https://github.com/your-org/docs \
  -e DB_TYPE=REDIS \
  -e REDIS_URL=redis://localhost:6379 \
  embed-job
```

In OpenShift, this is run as a Kubernetes `Job` with the appropriate environment configured via `ConfigMap` or `Secret`.

---

## 📂 Structure

```
.
├── embed_documents.py      # Main job script
├── entrypoint.sh           # Entrypoint for cloning and running the job
├── config.py               # Chunking config and default URLs
├── utils.py                # Shared utilities (e.g., env validation)
├── loaders/                # PDF and web document loaders
├── vector_db/              # Provider implementations per backend
├── requirements.txt        # Direct dependencies
└── redis_schema.yaml       # Redis-specific schema definition
```

---

## 🧪 Development

You can run the job locally with:

```bash
python embed_documents.py
```

Just make sure to export the appropriate environment variables before doing so.

---

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain)
- [Hugging Face Sentence Transformers](https://www.sbert.net/)
- [OpenShift UBI images](https://catalog.redhat.com/software/containers/search)
