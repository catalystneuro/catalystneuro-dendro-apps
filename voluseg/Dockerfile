# FROM ghcr.io/mikarubi/voluseg/voluseg:docs
FROM python:3.12.4-slim

# Install git
RUN apt-get update && apt-get install -y git

# Install dendro from github
RUN mkdir -p /src
WORKDIR /src
RUN git clone https://github.com/magland/dendro \
    && cd dendro \
    && cd python \
    && pip install -e .

# Install lindi
RUN pip install lindi

# Install pynwb
RUN pip install pynwb==2.8.3

# Copy files into the container
COPY *.py /app/

# Set the working directory
WORKDIR /app