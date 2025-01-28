FROM python:3.9-slim

# Install git and clean up in one layer to keep image size down
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages in one layer
RUN pip install --no-cache-dir \
    lindi \
    pynwb==2.8.1 \
    remfile \
    h5py \
    photon_flux_estimation

# Install dendro from github
RUN mkdir -p /src && \
    cd /src && \
    git clone https://github.com/magland/dendro && \
    cd dendro/python && \
    pip install -e .

# Create app directory and set as working directory
WORKDIR /app

# Copy Python files into the container
COPY *.py /app/
