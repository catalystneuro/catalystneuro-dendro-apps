FROM python:3.9-slim

# Install git and clean up in one layer to keep image size down
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages in one layer
RUN pip install --no-cache-dir \
    pynwb==2.8.1 \
    remfile==0.1.13 \
    h5py==3.12.1 \
    photon_flux_estimation==0.1.0

# Install dendro
RUN pip install dendro==0.6.20
# RUN mkdir -p /src && \
#     cd /src && \
#     git clone https://github.com/magland/dendro && \
#     cd dendro/python && \
#     pip install -e .

# Create app directory and set as working directory
WORKDIR /app

# Copy Python files into the container
COPY *.py /app/
