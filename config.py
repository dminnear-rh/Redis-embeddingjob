import os

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1024))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 40))
DB_TYPE = os.getenv("DB_TYPE", "REDIS")

DEFAULT_WEB_URLS = [
    "https://ai-on-openshift.io/getting-started/openshift/",
    "https://ai-on-openshift.io/getting-started/opendatahub/",
    "https://ai-on-openshift.io/getting-started/openshift-ai/",
    "https://ai-on-openshift.io/odh-rhoai/configuration/",
    "https://ai-on-openshift.io/odh-rhoai/custom-notebooks/",
    "https://ai-on-openshift.io/odh-rhoai/nvidia-gpus/",
    "https://ai-on-openshift.io/odh-rhoai/custom-runtime-triton/",
    "https://ai-on-openshift.io/odh-rhoai/openshift-group-management/",
    "https://ai-on-openshift.io/tools-and-applications/minio/minio/",
]

web_urls_env = os.getenv("WEB_URLS")

WEB_URLS = (
    [url.strip() for url in web_urls_env.split(",") if url.strip()]
    if web_urls_env
    else DEFAULT_WEB_URLS
)
