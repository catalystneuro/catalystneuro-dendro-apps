FROM ghcr.io/mikarubi/voluseg/voluseg:dev

# Install git
RUN apt-get update && apt-get install -y git

RUN mkdir -p /src
WORKDIR /src

# Install dendro
RUN pip install dendro==0.6.20
# RUN git clone https://github.com/magland/dendro \
#     && cd dendro \
#     && cd python \
#     && pip install -e .

# Install lindi
RUN pip install lindi

# Install pynwb
RUN pip install pynwb==2.8.1

# Copy files into the container
COPY *.py /app/

# Set the working directory
WORKDIR /app