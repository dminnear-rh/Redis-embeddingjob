#!/usr/bin/env bash

set -e

# Required
: "${DOC_GIT_REPO:?DOC_GIT_REPO is required}"

# Optional with defaults
: "${TEMP_DIR:=/tmp}"
: "${DOC_LOCATION:=}"

# Prepare destination path
REPO_PATH="${TEMP_DIR}/source_repo"
mkdir -p "$REPO_PATH"

# Clone PDF docs source
echo "Cloning repository $DOC_GIT_REPO to $REPO_PATH"
git clone --depth 1 "$DOC_GIT_REPO" "$REPO_PATH"

# Build and export full document path for the embedding job
export PDF_FOLDER="${REPO_PATH}/${DOC_LOCATION}"
echo "Resolved PDF_FOLDER: $PDF_FOLDER"

# Run the embedding script
python -u ./embed_documents.py
