#!/bin/bash

source /root/miniconda3/bin/activate
conda activate dev
echo "Using Conda env: $CONDA_DEFAULT_ENV"

echo "DOC_GIT_REPO  : $DOC_GIT_REPO"
echo "DOC_LOCATION  : $DOC_LOCATION"
echo "TEMP_DIR      : $TEMP_DIR"

if [ -z ${DOC_GIT_REPO+x} ]; then
    echo "Provide GIT repository location"
    exit 1
fi
if [ -z ${DOC_LOCATION+x} ]; then
    echo "Document location is not set. Provide location inside directory"
    exit 1
fi

mkdir ${TEMP_DIR}/source_repo
git clone ${DOC_GIT_REPO} ${TEMP_DIR}/source_repo

python -u  ./Langchain-Redis-Ingest.py
