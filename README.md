# CatalystNeuro Dendro Apps

A collection of neuroimaging analysis applications designed to run on the Dendro platform, providing scalable cloud-based processing for neuroscience data.

## Overview

This repository contains containerized neuroimaging processors that can be deployed and executed through the Dendro distributed computing platform. Each application is designed to process neuroscience data stored in NWB (Neurodata Without Borders) format and can be scaled across cloud computing resources.

## Applications

### 🔬 [Voluseg](./voluseg/) - Volumetric Segmentation

Automated segmentation and analysis of volumetric calcium imaging data for identifying individual neurons in 3D brain volumes.

- **Input**: NWB files with volumetric imaging data
- **Output**: Segmented cell data in NWB format
- **Use Case**: Two-photon and light-sheet microscopy cell segmentation

📖 **[View detailed documentation](./voluseg/README.md)**

### ⚡ [Photon Flux](./photon_flux/) - Two-Photon Sensitivity Estimation

Estimates photon flux and sensitivity parameters for two-photon imaging data to assess data quality and optimize imaging parameters.

- **Input**: NWB files with two-photon imaging series
- **Output**: Photon flux analysis results in JSON format
- **Use Case**: Data quality assessment

📖 **[View detailed documentation](./photon_flux/README.md)**

## Quick Start

### Prerequisites

- Python 3.8+
- Access to a Dendro service
- NWB-formatted neuroscience data

### Installation

1. Clone this repository:
```bash
git clone https://github.com/catalystneuro/catalystneuro-dendro-apps.git
cd catalystneuro-dendro-apps
```

2. Install the Dendro Python client:
```bash
pip install dendro-python-client
```

### Basic Usage

```python
from dendro.client import submit_job, DendroJobDefinition, DendroJobRequiredResources

# Example: Submit a Voluseg job
job_def = DendroJobDefinition(
    appName="voluseg",
    processorName="voluseg_processor",
    inputFiles=[...],  # Your NWB input files
    outputFiles=[...], # Output configuration
    parameters=[...]   # Processing parameters
)

job = submit_job(
    service_name="your-service-name",
    job_definition=job_def,
    required_resources=DendroJobRequiredResources(...)
)
```

For detailed usage examples and parameter descriptions, see the individual application documentation.

## Repository Structure

```
catalystneuro-dendro-apps/
├── voluseg/                    # Voluseg application
│   ├── README.md              # Detailed Voluseg documentation
│   ├── Dockerfile             # Container definition
│   ├── main.py               # Application entry point
│   ├── spec.json             # Processor specification
│   └── VolusegProcessor.py   # Core processing logic
├── photon_flux/               # Photon flux application
│   ├── README.md              # Detailed Photon Flux documentation
│   ├── Dockerfile            # Container definition
│   ├── main.py              # Application entry point
│   ├── spec.json            # Processor specification
│   └── PhotonFlux.py        # Core processing logic
├── examples/                  # Usage examples
│   ├── example_1.py          # Voluseg example
│   └── example_photon_flux.py # Photon flux example
├── compute_client/           # Compute client configuration
└── README.md                # This file
```

## Docker Images

Pre-built Docker images are available for both applications:

- **Voluseg**: `ghcr.io/catalystneuro/dendro-voluseg:latest`
- **Photon Flux**: `ghcr.io/catalystneuro/dendro-photon_flux:latest`

## Data Compatibility

These applications work with:
- **NWB (Neurodata Without Borders)** format files
- **LINDI** (Linked Data Interface) format for efficient cloud access
- Data from **DANDI Archive** and other NWB-compatible repositories

## Examples

Working examples for both applications are available in the [`examples/`](./examples/) directory:

- [`example_1.py`](./examples/example_1.py) - Voluseg volumetric segmentation
- [`example_photon_flux.py`](./examples/example_photon_flux.py) - Photon flux analysis

## Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions or support:
- Open an issue on this repository
- Visit the [CatalystNeuro website](https://www.catalystneuro.com/)
- Check the [Dendro platform documentation](https://dendro.vercel.app/)

## Acknowledgments

Developed by [CatalystNeuro](https://www.catalystneuro.com/) for the neuroscience community.
