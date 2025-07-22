# Photon Flux - Two-Photon Sensitivity Estimation

Estimates photon flux and sensitivity parameters for two-photon imaging data to assess data quality and optimize imaging parameters.

## Overview

Photon Flux is a specialized tool for analyzing two-photon microscopy data to estimate photon flux and sensitivity parameters. This analysis is crucial for assessing data quality, optimizing imaging parameters, and ensuring reliable quantitative measurements in calcium imaging experiments.

## Key Features

- **Photon flux estimation** for two-photon microscopy data
- **Frame subset analysis** for efficient processing of large datasets
- **Edge cropping capabilities** to remove imaging artifacts
- **Movie transposition support** for proper data orientation
- **Quality assessment metrics** for imaging data validation
- **NWB format compatibility** for standardized neuroscience data

## Input/Output

- **Input**: NWB files containing two-photon imaging series (`.nwb` or `.nwb.lindi.tar` format)
- **Output**: Photon flux analysis results in JSON format

## Parameters

### Required Parameters

- **`series_path`** (str): Path to the multiphoton series within the NWB file
  - Example: "acquisition/TwoPhotonSeries1"
  - This specifies which imaging series to analyze within the NWB file

### Processing Parameters

- **`subset_frames`** (List[int]): Indices of frames to use for sensitivity estimation
  - Example: `[0, 1, 2, ..., 499]` for first 500 frames
  - Allows analysis of specific time periods or reduced datasets for efficiency
  - Can be used to avoid motion artifacts or focus on specific experimental periods

- **`crop_edges`** (List[int]): Number of pixels to crop from each edge of the frames
  - Format: `[top, bottom, left, right]`
  - Example: `[4, 4, 4, 4]` removes 4 pixels from each edge
  - Helps remove edge artifacts common in two-photon imaging
  - Reduces noise from laser scanning artifacts at frame boundaries

- **`transpose_movie`** (bool): Whether to transpose the movie data
  - Default: depends on data orientation
  - The photon flux estimation requires movies in shape (frames, height, width)
  - Set to `true` if your data is in (height, width, frames) format

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

# Configure photon flux analysis job
parameters_dict = {
    "series_path": "acquisition/TwoPhotonSeries1",
    "subset_frames": list(range(500)),  # Analyze first 500 frames
    "crop_edges": [4, 4, 4, 4],        # Remove 4 pixels from each edge
    "transpose_movie": False,           # Keep original orientation
}

job_def = DendroJobDefinition(
    appName="photon_flux",
    processorName="photon_flux_processor",
    inputFiles=[
        DendroJobInputFile(
            name="input",
            fileBaseName="your_twophoton_data.nwb",
            url="https://your-data-url.com/file.nwb",
        )
    ],
    outputFiles=[
        DendroJobOutputFile(
            name="output",
            fileBaseName="photon_flux_results.json",
        )
    ],
    parameters=[
        DendroJobParameter(name=k, value=v) for k, v in parameters_dict.items()
    ],
)

# Resource requirements for photon flux analysis
required_resources = DendroJobRequiredResources(
    numCpus=2,         # Moderate CPU requirements
    numGpus=0,         # CPU-only processing
    memoryGb=4,        # Relatively low memory requirements
    timeSec=3600,      # 1 hour processing time
)

# Submit the job
job = submit_job(
    service_name="photon_flux",
    job_definition=job_def,
    required_resources=required_resources,
    target_compute_client_ids=["*"],
    tags=["photon_flux", "quality_assessment"],
    skip_cache=False,
)

print(f"Job submitted: {job.job_url}")
print(f"Status: {job.status}")
```

## Resource Requirements

### Recommended Resources
- **CPU**: 2-4 cores (analysis is not heavily parallelized)
- **Memory**: 4-16 GB RAM depending on dataset size
- **Storage**: Minimal additional storage beyond input data

### Scaling Guidelines
- Processing time scales with number of frames analyzed
- Memory requirements depend on frame size and subset selection
- Cropping edges can reduce memory usage and processing time

## Docker Image

The Photon Flux processor is available as a pre-built Docker image:
```
ghcr.io/catalystneuro/dendro-photon_flux:latest
```

## Data Requirements

### Input Data Format
- NWB files containing two-photon calcium imaging data
- Supported formats: `.nwb`, `.nwb.lindi.tar`
- Data should be organized as TwoPhotonSeries objects within the NWB file

### Expected Data Structure
- Two-photon imaging series with proper temporal sampling information
- Multi-dimensional arrays with shape (frames, height, width) or (height, width, frames)
- Proper metadata including imaging parameters and timestamps

### Data Quality Considerations
- Higher signal-to-noise ratio data will yield more accurate photon flux estimates
- Avoid frames with significant motion artifacts for best results
- Ensure consistent imaging conditions across analyzed frames

## Output Description

The output JSON file contains:
- **Photon flux estimates**: Quantitative measures of photon detection efficiency
- **Sensitivity parameters**: Metrics related to imaging system performance
- **Quality metrics**: Assessment of data quality and reliability
- **Processing metadata**: Information about analysis parameters and conditions

### Interpreting Results
- Higher photon flux values generally indicate better signal quality
- Sensitivity parameters help optimize imaging settings for future experiments
- Quality metrics can identify potential issues with imaging conditions

## Use Cases

### Data Quality Assessment
- Evaluate imaging system performance
- Compare different imaging conditions or setups
- Identify optimal imaging parameters for specific experiments

### Experimental Optimization
- Determine appropriate laser power settings
- Optimize exposure times and frame rates
- Assess trade-offs between signal quality and photobleaching

### Quantitative Analysis Preparation
- Validate data quality before downstream analysis
- Ensure consistent imaging conditions across experimental sessions
- Identify frames suitable for quantitative measurements

## Best Practices

1. **Frame Selection**: Choose representative frames that avoid motion artifacts
2. **Edge Cropping**: Remove sufficient edge pixels to eliminate scanning artifacts
3. **Parameter Documentation**: Record analysis parameters for reproducibility
4. **Quality Control**: Review output metrics to ensure reliable results
