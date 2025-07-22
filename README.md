# CatalystNeuro Dendro Apps

A collection of neuroimaging analysis applications designed to run on the Dendro platform, providing scalable cloud-based processing for neuroscience data.

## Overview

This repository contains containerized neuroimaging processors that can be deployed and executed through the Dendro distributed computing platform. Each application is designed to process neuroscience data stored in NWB (Neurodata Without Borders) format and can be scaled across cloud computing resources.

## Applications

### 🔬 Voluseg - Volumetric Segmentation

**Purpose**: Automated segmentation and analysis of volumetric calcium imaging data for identifying individual neurons in 3D brain volumes.

**Key Features**:
- Volumetric cell segmentation for two-photon and light-sheet microscopy data
- Motion correction and registration capabilities
- Flexible detrending options (standard, robust, or none)
- Configurable registration quality levels (high, medium, low, none)
- Parallel processing support for improved performance
- Support for multi-color imaging data

**Input**: NWB files containing volumetric imaging data (`.nwb` or `.nwb.lindi.tar` format)
**Output**: Segmented cell data in NWB format (`.lindi.tar` format)

**Key Parameters**:
- `diam_cell`: Expected cell diameter in microns (default: 6.0)
- `registration`: Registration quality level
- `detrending`: Type of signal detrending to apply
- `f_volume`: Imaging frequency in Hz
- `timepoints`: Number of timepoints for segmentation analysis

### ⚡ Photon Flux - Two-Photon Sensitivity Estimation

**Purpose**: Estimates photon flux and sensitivity parameters for two-photon imaging data to assess data quality and optimize imaging parameters.

**Key Features**:
- Photon flux estimation for two-photon microscopy data
- Frame subset analysis for efficient processing
- Edge cropping capabilities to remove artifacts
- Movie transposition support for proper data orientation
- Quality assessment metrics for imaging data

**Input**: NWB files containing two-photon imaging series (`.nwb` or `.nwb.lindi.tar` format)
**Output**: Photon flux analysis results in JSON format

**Key Parameters**:
- `series_path`: Path to the multiphoton series within the NWB file
- `subset_frames`: Specific frame indices to analyze
- `crop_edges`: Number of pixels to crop from each edge [top, bottom, left, right]
- `transpose_movie`: Whether to transpose movie data for proper orientation

## Getting Started

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

2. Install the required dependencies:
```bash
pip install dendro-python-client
```

### Usage Examples

#### Running Voluseg Analysis

```python
from dendro.client import submit_job, DendroJobDefinition, DendroJobRequiredResources

# Configure voluseg job
job_def = DendroJobDefinition(
    appName="voluseg",
    processorName="voluseg_processor",
    inputFiles=[...],  # Your NWB input files
    outputFiles=[...], # Output configuration
    parameters=[
        DendroJobParameter(name="registration", value="high"),
        DendroJobParameter(name="diam_cell", value=5.0),
        DendroJobParameter(name="f_volume", value=2.0),
    ]
)

# Submit job with resource requirements
job = submit_job(
    service_name="your-service-name",
    job_definition=job_def,
    required_resources=DendroJobRequiredResources(
        numCpus=24,
        numGpus=0,
        memoryGb=120,
        timeSec=6 * 3600
    )
)
```

#### Running Photon Flux Analysis

```python
# Configure photon flux job
job_def = DendroJobDefinition(
    appName="photon_flux",
    processorName="photon_flux_processor",
    inputFiles=[...],  # Your NWB input files
    outputFiles=[...], # Output configuration
    parameters=[
        DendroJobParameter(name="series_path", value="acquisition/TwoPhotonSeries1"),
        DendroJobParameter(name="subset_frames", value=list(range(500))),
        DendroJobParameter(name="crop_edges", value=[4, 4, 4, 4]),
    ]
)

# Submit with lighter resource requirements
job = submit_job(
    service_name="photon_flux",
    job_definition=job_def,
    required_resources=DendroJobRequiredResources(
        numCpus=2,
        numGpus=0,
        memoryGb=4,
        timeSec=3600
    )
)
```

## Repository Structure

```
catalystneuro-dendro-apps/
├── voluseg/                    # Voluseg application
│   ├── Dockerfile             # Container definition
│   ├── main.py               # Application entry point
│   ├── spec.json             # Processor specification
│   └── VolusegProcessor.py   # Core processing logic
├── photon_flux/               # Photon flux application
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

Both applications are available as pre-built Docker images:

- **Voluseg**: `ghcr.io/catalystneuro/dendro-voluseg:latest`
- **Photon Flux**: `ghcr.io/catalystneuro/dendro-photon_flux:latest`

## Data Compatibility

These applications are designed to work with:
- **NWB (Neurodata Without Borders)** format files
- **LINDI** (Linked Data Interface) format for efficient cloud access
- Data from **DANDI Archive** and other NWB-compatible repositories

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
