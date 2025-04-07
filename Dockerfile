FROM registry.access.redhat.com/ubi9/ubi:9.5

# Install system dependencies and Microsoft ODBC Driver 18 for SQL Server
RUN dnf install -y \
    wget \
    git \
    unixODBC \
    unixODBC-devel && \
    curl -sSL https://packages.microsoft.com/config/rhel/9/prod.repo -o /etc/yum.repos.d/mssql-release.repo && \
    ACCEPT_EULA=Y dnf install -y msodbcsql18 && \
    dnf clean all

# Install Miniconda
RUN mkdir -p ~/miniconda3 && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh && \
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && \
    rm ~/miniconda3/miniconda.sh && \
    ~/miniconda3/bin/conda update -n base -c defaults conda -y

# Set working directory
WORKDIR /app

# Copy environment file and create Conda environment
COPY environment.yaml .
RUN ~/miniconda3/bin/conda env create -f /app/environment.yaml

# Copy application files
COPY vector_db .
COPY Langchain-Redis-Ingest.py .
COPY redis_schema.yaml .
COPY entrypoint.sh .

# Set permissions and switch to non-root user
RUN chmod -R 777 . && \
    chown 1001:0 ./*

USER 1001

ENTRYPOINT [ "/usr/bin/bash", "/app/entrypoint.sh" ]
