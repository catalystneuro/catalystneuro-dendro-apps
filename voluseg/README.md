# Voluseg - Volumetric Segmentation

Automated segmentation and analysis of volumetric calcium imaging data for identifying individual neurons in 3D brain volumes.

## Overview

Voluseg is a powerful tool for processing volumetric calcium imaging data from two-photon and light-sheet microscopy. It performs automated cell segmentation, motion correction, and signal extraction from 3D brain imaging datasets.

## Key Features

- **Volumetric cell segmentation** for two-photon and light-sheet microscopy data
- **Motion correction and registration** with configurable quality levels
- **Flexible detrending options** (standard, robust, or none)
- **Parallel processing support** for improved performance
- **Multi-color imaging support** for complex experimental designs
- **NWB format compatibility** for standardized neuroscience data

## Input/Output

- **Input**: NWB files containing volumetric imaging data (`.nwb` or `.nwb.lindi.tar` format)
- **Output**: Segmented cell data in NWB format (`.lindi.tar` format)

## Parameters

### Core Parameters

- **`diam_cell`** (float, default: 6.0): Expected cell diameter in microns
- **`registration`** (str, default: "medium"): Registration quality level
  - Options: "high", "medium", "low", "none"
- **`detrending`** (str, default: "standard"): Type of signal detrending
  - Options: "standard", "robust", "none"
- **`f_volume`** (float, default: 2.0): Imaging frequency in Hz
- **`timepoints`** (int, default: 1000): Number of timepoints for segmentation analysis

### Advanced Parameters

- **`ds`** (int, default: 2): Spatial coarse-graining in x-y dimension
- **`planes_pad`** (int, default: 0): Number of planes to pad for robust registration
- **`planes_packed`** (bool, default: false): Packed planes in each volume
- **`parallel_clean`** (bool, default: true): Parallelization of final cleaning
- **`parallel_volume`** (bool, default: true): Parallelization of mean-volume computation
- **`save_volume`** (bool, default: false): Save registered volumes after segmentation

### Signal Processing Parameters

- **`type_timepoints`** (str, default: "dff"): Type of timepoints for cell detection
  - Options: "dff", "periodic", "custom"
- **`type_mask`** (str, default: "geomean"): Type of volume averaging for mask
  - Options: "mean", "geomean", "max"
- **`f_hipass`** (float, default: 0): Frequency (Hz) for high-pass filtering
- **`t_baseline`** (int, default: 300): Interval for baseline calculation in seconds
- **`t_section`** (float, default: 0.01): Exposure time in seconds for slice acquisition
- **`thr_mask`** (float, default: 0.5): Threshold for volume mask

### Spatial Resolution Parameters

- **`res_x`** (float, default: 0.40625): X resolution in microns
- **`res_y`** (float, default: 0.40625): Y resolution in microns
- **`res_z`** (float, default: 5.0): Z resolution in microns

### Processing Parameters

- **`n_cells_block`** (int, default: 316): Number of cells in a block
- **`n_colors`** (int, default: 1): Number of brain colors (2 for two-color volumes)
- **`registration_restrict`** (str, default: ""): Restrict registration pattern
- **`dim_order`** (str, default: "xyz"): Dimensions order (e.g., "zyx", "xyz")
- **`ext`** (str, default: ".nwb"): File extension
- **`remote`** (bool, default: true): Remote file processing
- **`output_to_nwb`** (bool, default: true): Save results to a new NWB file

## Usage Example

```python
from dendro.client import (
    submit_job,
    DendroJobDefinition,
    DendroJobRequiredResources,
    DendroJobParameter,
    DendroJobInputFile,
    DendroJobOutputFile,
)

# Configure voluseg job
parameters_dict = {
    "registration": "high",
    "diam_cell": 5.0,
    "f_volume": 2.0,
    "timepoints": 1000,
    "detrending": "standard",
    "parallel_clean": True,
    "parallel_volume": True,
}

job_def = DendroJobDefinition(
    appName="voluseg",
    processorName="voluseg_processor",
    inputFiles=[
        DendroJobInputFile(
            name="input",
            fileBaseName="your_data.nwb",
            url="https://your-data-url.com/file.nwb",
        )
    ],
    outputFiles=[
        DendroJobOutputFile(
            name="output",
            fileBaseName="segmented_cells.nwb",
        )
    ],
    parameters=[
        DendroJobParameter(name=k, value=v) for k, v in parameters_dict.items()
    ],
)

# Resource requirements for typical voluseg job
required_resources = DendroJobRequiredResources(
    numCpus=24,        # High CPU count for parallel processing
    numGpus=0,         # CPU-only processing
    memoryGb=120,      # Large memory for volumetric data
    timeSec=6 * 3600,  # 6 hours processing time
)

# Submit the job
job = submit_job(
    service_name="your-service-name",
    job_definition=job_def,
    required_resources=required_resources,
    target_compute_client_ids=["*"],
    tags=["voluseg", "segmentation"],
    skip_cache=False,
)

print(f"Job submitted: {job.job_url}")
print(f"Status: {job.status}")
```

## Resource Requirements

### Recommended Resources
- **CPU**: 16-32 cores for optimal parallel processing
- **Memory**: 64-128 GB RAM depending on dataset size
- **Storage**: Sufficient space for input data and intermediate processing files
- **Time**: 2-8 hours depending on dataset size and parameters

### Scaling Guidelines
- Larger volumes require more memory and processing time
- Higher registration quality increases computational requirements
- Parallel processing options can significantly speed up analysis but require more memory

## Docker Image

The Voluseg processor is available as a pre-built Docker image:
```
ghcr.io/catalystneuro/dendro-voluseg:latest
```

## Data Requirements

### Input Data Format
- NWB files containing volumetric calcium imaging data
- Supported formats: `.nwb`, `.nwb.lindi.tar`
- Data should include proper spatial and temporal metadata

### Expected Data Structure
- Multi-dimensional arrays with shape (time, z, y, x) or similar
- Proper spatial resolution metadata (microns per pixel)
- Temporal sampling rate information

## Output Description

The output contains:
- **Segmented cell masks**: 3D regions of interest for each identified cell
- **Cell timeseries**: Extracted fluorescence traces for each cell
- **Quality metrics**: Assessment of segmentation quality
- **Registration information**: Motion correction parameters and results

