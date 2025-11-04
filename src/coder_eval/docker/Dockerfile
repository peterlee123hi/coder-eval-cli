FROM python:3.10-slim

# Prevent Python from writing .pyc files and force unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps required by Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    pytest \
    numpy \
    pandas \
    scipy \
    sympy \
    matplotlib \
    networkx \
    requests \
    beautifulsoup4 \
    tqdm \
    Pillow \
    lxml \
    timeout-decorator

# Default workspace (CLI mounts the code here)
WORKDIR /workspace
