# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables to prevent interactive prompts
ARG DEBIAN_FRONTEND=noninteractive

# Update package list and install necessary tools and dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    curl \
    gnupg \
    make \
    build-essential \
    pkg-config \
    libzmq3-dev \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libsqlite3-dev \
    libreadline-dev \
    libffi-dev \
    libbz2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.12.1 from source
RUN curl -fsSL "https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz" -o "Python-3.12.1.tgz" && \
    tar -xzf "Python-3.12.1.tgz" --strip-components=1 -C /usr/local/src && \
    cd /usr/local/src && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    ln -s /usr/local/bin/python3.12 /usr/local/bin/python3 && \
    ln -s /usr/local/bin/pip3.12 /usr/local/bin/pip3 && \
    cd / && \
    rm -rf /usr/local/src "Python-3.12.1.tgz"

# Verify installation
RUN python3 --version && pip3 --version

